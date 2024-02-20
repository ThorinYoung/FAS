import torch
from PIL import Image
import torchvision.transforms as transforms
from sr_models.SRGAN_model import SRGANModel
import numpy as np
import argparse

# here transform mean is fine-tuned, before is 0.5 * 3
_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.515, 0.53, 0.55], std=[0.5, 0.5, 0.5])])


def get_FaceSR_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu_ids', type=str, default=None)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--lr_G', type=float, default=1e-4)
    parser.add_argument('--weight_decay_G', type=float, default=0)
    parser.add_argument('--beta1_G', type=float, default=0.9)
    parser.add_argument('--beta2_G', type=float, default=0.99)
    parser.add_argument('--lr_D', type=float, default=1e-4)
    parser.add_argument('--weight_decay_D', type=float, default=0)
    parser.add_argument('--beta1_D', type=float, default=0.9)
    parser.add_argument('--beta2_D', type=float, default=0.99)
    parser.add_argument('--lr_scheme', type=str, default='MultiStepLR')
    parser.add_argument('--niter', type=int, default=100000)
    parser.add_argument('--warmup_iter', type=int, default=-1)
    parser.add_argument('--lr_steps', type=list, default=[50000])
    parser.add_argument('--lr_gamma', type=float, default=0.5)
    parser.add_argument('--pixel_criterion', type=str, default='l1')
    parser.add_argument('--pixel_weight', type=float, default=1e-2)
    parser.add_argument('--feature_criterion', type=str, default='l1')
    parser.add_argument('--feature_weight', type=float, default=1)
    parser.add_argument('--gan_type', type=str, default='ragan')
    parser.add_argument('--gan_weight', type=float, default=5e-3)
    parser.add_argument('--D_update_ratio', type=int, default=1)
    parser.add_argument('--D_init_iters', type=int, default=0)

    parser.add_argument('--print_freq', type=int, default=100)
    parser.add_argument('--val_freq', type=int, default=1000)
    parser.add_argument('--save_freq', type=int, default=10000)
    parser.add_argument('--crop_size', type=float, default=0.85)
    parser.add_argument('--lr_size', type=int, default=128)
    parser.add_argument('--hr_size', type=int, default=512)

    # network G
    parser.add_argument('--which_model_G', type=str, default='RRDBNet')
    parser.add_argument('--G_in_nc', type=int, default=3)
    parser.add_argument('--out_nc', type=int, default=3)
    parser.add_argument('--G_nf', type=int, default=64)
    parser.add_argument('--nb', type=int, default=16)

    # network D
    parser.add_argument('--which_model_D', type=str, default='discriminator_vgg_128')
    parser.add_argument('--D_in_nc', type=int, default=3)
    parser.add_argument('--D_nf', type=int, default=64)

    # data dir
    parser.add_argument('--pretrain_model_G', type=str, default='checkpoint/90000_G.pth')
    parser.add_argument('--pretrain_model_D', type=str, default=None)

    args = parser.parse_args()

    return args


class SR:
    def __init__(self):
        self.sr_model = SRGANModel(get_FaceSR_opt(), is_train=False)
        self.sr_model.load()

    def sr_forward(self, img, padding=0.5, moving=0.1):
        # img_aligned, M = dlib_detect_face(img, padding=padding, image_size=(128, 128), moving=moving)
        # input_img = torch.unsqueeze(_transform(Image.fromarray(img_aligned)), 0)
        # self.sr_model.var_L = input_img.to(self.sr_model.device)
        input_img = torch.unsqueeze(_transform(Image.fromarray(img)), 0)
        self.sr_model.var_L = input_img.to(self.sr_model.device)
        self.sr_model.test()
        output_img = self.sr_model.fake_H.squeeze(0).cpu().numpy()
        output_img = np.clip((np.transpose(output_img, (1, 2, 0)) / 2.0 + 0.5) * 255.0, 0, 255).astype(np.uint8)
        # rec_img = face_recover(output_img, M * 4, img)
        rec_img = None
        return output_img, rec_img

