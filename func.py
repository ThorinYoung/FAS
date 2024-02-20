import os
import pickle
import time

import PIL
import cv2
import yaml
from PyQt5.QtGui import QImage, QPixmap
from scipy.spatial import ConvexHull
from tqdm import tqdm
import imageio
import numpy as np
from skimage.transform import resize
from skimage import img_as_ubyte
import torch
import dnnlib
from dnnlib import tflib
from fomm_models.generator import OcclusionAwareGenerator
from fomm_models.keypoint_detector import KPDetector
from sr_models.sr import SR
from sync_batchnorm import DataParallelWithCallback


# save generate code, which can be modified to generate customized style
def text_save(file, data):
    for i in range(len(data[0])):
        s = str(data[0][i])+'\n'
        file.write(s)


# generate random image using random latent code
def generate_image(window):
    truncation_psi = 0.5
    noise_vars = [var for name, var in window.Gs.components.synthesis.vars.items() if name.startswith('noise')]
    Gs_kwargs = dnnlib.EasyDict()
    Gs_kwargs.output_transform = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
    Gs_kwargs.randomize_noise = True
    if truncation_psi is not None:
        Gs_kwargs.truncation_psi = truncation_psi
    z = np.random.randn(1, *window.Gs.input_shape[1:])  # [minibatch, component]
    # txt_filename = 'res/generate_codes/' + 'generate.txt'
    # os.makedirs('res/generate_codes', exist_ok=True)
    # with open(txt_filename, 'w') as f:
    #     text_save(f, z)
    window.latent = z
    tflib.set_vars({var: np.random.randn(*var.shape.as_list()) for var in noise_vars})  # [height, width]
    images = window.Gs.run(z, None, **Gs_kwargs)  # [minibatch, height, width, channel]
    result = PIL.Image.fromarray(images[0], 'RGB')
    window.image = result
    # save image
    # PIL.Image.fromarray(images[0], 'RGB').save(dnnlib.make_run_dir_path('res/' + 'generate.png'))
    # show image
    window.view.scale(1. / window.scale, 1. / window.scale)
    window.scale = min(window.view.width() / 1024, window.view.height() / 1024)
    window.view.scale(window.scale, window.scale)
    frame = QImage(images[0], 1024, 1024, QImage.Format_RGB888)
    window.scene.clear()
    pix = QPixmap.fromImage(frame)
    window.scene.addPixmap(pix)


# read feature from local file
def read_feature(window, file_name):
    file = open(file_name, mode='r')
    contents = file.readlines()
    code = np.zeros((512, ))
    for i in range(512):
        name = contents[i]
        name = name.strip('\n')
        code[i] = name
    i = 512
    while i < len(contents):
        if contents[i]:
            window.attr_ops.update({contents[i].strip(): float(contents[i+1].strip())})
            i += 2
    code = np.float32(code)
    file.close()
    return code


# change latent using specific npy file
def move_latent(latent_vector, window, Gs_syn_kwargs):
    # latent_vector是人脸潜编码，direction是人脸调整方向，coeffs是变化步幅的向量，generator是生成器
    ops = window.attr_ops
    # for i in range(len(window.attr_ops)):
    #     ops.update({window.attr_ops[i][0]: window.attr_ops[i][1]})
    new_latent_vector = latent_vector.copy()
    for key in ops.keys():
        direction = np.load(os.path.join(window.npy_path, window.attr2npy[key]))
        # os.makedirs('res/'+direction_file.split('.')[0], exist_ok=True)
        # for i, coeff in enumerate(coeffs):
        new_latent_vector[0][:8] = (new_latent_vector[0] - float(window.attr2slider[key].value())*direction)[:8]
    images = window.Gs.components.synthesis.run(new_latent_vector, **Gs_syn_kwargs)
    result = PIL.Image.fromarray(images[0], 'RGB')
    window.image = result
    # result.save('res/'+direction_file.split('.')[0]+'/'+str(i).zfill(3)+'.png')
    window.view.scale(1. / window.scale, 1. / window.scale)
    window.scale = min(window.view.width() / 1024, window.view.height() / 1024)
    window.view.scale(window.scale, window.scale)
    frame = QImage(images[0], 1024, 1024, QImage.Format_RGB888)
    window.scene.clear()
    pix = QPixmap.fromImage(frame)
    window.scene.addPixmap(pix)
    # window.update_command(f'editing image done!')


# edit image to target attribute
def edit_image(window):
    truncation_psi = 0.5
    w_avg = window.Gs.get_var('dlatent_avg')
    noise_vars = [var for name, var in window.Gs.components.synthesis.vars.items() if name.startswith('noise')]
    Gs_kwargs = dnnlib.EasyDict()
    Gs_kwargs.output_transform = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
    Gs_kwargs.randomize_noise = False
    Gs_kwargs.minibatch_size = 1
    if window.latent is None:
        face_latent = read_feature(window, window.save_name + '.txt')
        z = np.stack(face_latent for _ in range(1))
        window.latent = z
    else:
        z = window.latent
    tflib.set_vars({var: np.random.randn(*var.shape.as_list()) for var in noise_vars})  # [height, width]
    w = window.Gs.components.mapping.run(z, None)
    w = w_avg + (w - w_avg) * truncation_psi
    # coeffs = [-15., -12., -9., -6., -3., 0., 3., 6., 9., 12.]
    move_latent(w, window, Gs_kwargs)


def load_checkpoints(config_path, checkpoint_path, cpu=False):
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    generator = OcclusionAwareGenerator(**config['model_params']['generator_params'],
                                        **config['model_params']['common_params'])
    if not cpu:
        generator.cuda()

    kp_detector = KPDetector(**config['model_params']['kp_detector_params'],
                             **config['model_params']['common_params'])
    if not cpu:
        kp_detector.cuda()

    if cpu:
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    else:
        checkpoint = torch.load(checkpoint_path)

    generator.load_state_dict(checkpoint['generator'])
    kp_detector.load_state_dict(checkpoint['kp_detector'])

    if not cpu:
        generator = DataParallelWithCallback(generator)
        kp_detector = DataParallelWithCallback(kp_detector)

    generator.eval()
    kp_detector.eval()

    return generator, kp_detector


# normalize key point
def normalize_kp(kp_source, kp_driving, kp_driving_initial, adapt_movement_scale=False, use_relative_movement=False, use_relative_jacobian=False):
    if adapt_movement_scale:
        source_area = ConvexHull(kp_source['value'][0].data.cpu().numpy()).volume
        driving_area = ConvexHull(kp_driving_initial['value'][0].data.cpu().numpy()).volume
        adapt_movement_scale = np.sqrt(source_area) / np.sqrt(driving_area)
    else:
        adapt_movement_scale = 1

    kp_new = {k: v for k, v in kp_driving.items()}

    if use_relative_movement:
        kp_value_diff = (kp_driving['value'] - kp_driving_initial['value'])
        kp_value_diff *= adapt_movement_scale
        kp_new['value'] = kp_value_diff + kp_source['value']

        if use_relative_jacobian:
            jacobian_diff = torch.matmul(kp_driving['jacobian'], torch.inverse(kp_driving_initial['jacobian']))
            kp_new['jacobian'] = torch.matmul(jacobian_diff, kp_source['jacobian'])

    return kp_new


def generate_animation(window, predictions, frame_count, source_image, driving_video, generator, kp_detector, relative=True, adapt_movement_scale=True, cpu=False):
    with torch.no_grad():
        source = torch.tensor(source_image[np.newaxis].astype(np.float32)).permute(0, 3, 1, 2)
        if not cpu:
            source = source.cuda()
        driving = torch.tensor(np.array(driving_video)[np.newaxis].astype(np.float32)).permute(0, 4, 1, 2, 3)
        kp_source = kp_detector(source)
        kp_driving_initial = kp_detector(driving[:, :, 0])
        count = 0

        # default size is 256, super-resolution size is 1024
        window.view.scale(1./window.scale, 1./window.scale)
        if not window.vid_sr.isChecked():
            window.scale = min(window.view.width() / 256, window.view.height() / 256)
        else:
            window.scale = min(window.view.width() / 1024, window.view.height() / 1024)
        window.view.scale(window.scale, window.scale)

        sr = SR()
        for frame_idx in tqdm(range(driving.shape[2])):
            # .cuda() moved upper
            driving_frame = driving[:, :, frame_idx].cuda()
            # if not cpu:
            # driving_frame = driving_frame.cuda()
            # detect key points
            kp_driving = kp_detector(driving_frame)
            # normalize key points
            kp_norm = normalize_kp(kp_source=kp_source, kp_driving=kp_driving,
                                   kp_driving_initial=kp_driving_initial, use_relative_movement=relative,
                                   use_relative_jacobian=relative, adapt_movement_scale=adapt_movement_scale)
            out = generator(source, kp_source=kp_source, kp_driving=kp_norm)
            predictions.append(np.transpose(out['prediction'].data.cpu().numpy(), [0, 2, 3, 1])[0])
            count += 1
            im = img_as_ubyte(predictions[-1])
            if window.vid_sr.isChecked():
                # img = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                im, _ = sr.sr_forward(im)
                predictions[-1] = im
                x, y = im.shape[:-1]
            else:
                y, x = im.shape[:-1]
            # use .copy()
            frame = QImage(im.copy(), x, y, QImage.Format_RGB888)
            window.scene.clear()
            pix = QPixmap.fromImage(frame)
            window.scene.addPixmap(pix)
            window.update_command(f'generating frame: {count} / {frame_count}...')
    window.vid_finish_flag = 1
    return predictions
