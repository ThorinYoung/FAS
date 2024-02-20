import gc
import multiprocessing
import os
import pickle
import sys
import threading
from time import sleep
from multiprocessing import Process
import multiprocess
from PyQt5 import QtCore, QtGui
from numba import cuda
import PIL
import tensorflow as tf
from func import *
from PIL import Image
from tqdm import tqdm
import torch
import numpy as np
import stylegan2_models.dnnlib as dnnlib
import stylegan2_models.dnnlib.tflib as tflib
from stylegan2_models import loader
from sync_batchnorm import DataParallelWithCallback
import yaml
from skimage.transform import resize
from skimage import img_as_ubyte
import cv2
import imageio
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from sr_models.sr import SR
from main_window import MainWindow, Ui_Dialog


class Main(MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        # configs
        # 对话框
        self.d = dialogUi()
        # 源图像
        self.src_img = None
        # 驱动视频
        self.src_vid = None
        # 默认保存目录
        self.vid_save_path = 'res'
        # 是否保存图像（选项）
        self.img_save_flag = False
        # config目录
        self.config_path = os.path.join(os.path.dirname(__file__),'config')
        # checkpoint目录
        self.checkpoint_path = os.path.join(os.path.dirname(__file__),'checkpoint')
        # 驱动视频配置文件
        self.vid_yaml_path = os.path.join(self.config_path, 'vox-256.yaml')
        # 驱动视频checkpoint文件
        self.vid_checkpoint = os.path.join(self.checkpoint_path, 'vox-cpk.pth.tar')
        # 显示图像的组件scene
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        # QGraphicsview放缩（记录以便于下一次放缩）
        self.scale = 1
        self.vid_finish_flag = 0
        # 编辑图像的npy文件目录
        self.npy_path = 'stylegan2_models/latent_directions'
        # 属性到npy文件的映射
        self.attr2npy = {
            'age': 'age.npy',
            'ah': 'angle_horizontal.npy',
            'av': 'angle_vertical.npy',
            'beauty': 'beauty.npy',
            'angry': 'emotion_angry.npy',
            'disgust': 'emotion_disgust.npy',
            'easy': 'emotion_easy.npy',
            'fear': 'emotion_fear.npy',
            'happy': 'emotion_happy.npy',
            'sad': 'emotion_sad.npy',
            'surprise': 'emotion_surprise.npy',
            'eyeopen': 'eyes_open.npy',
            'faceshape': 'face_shape.npy',
            'gender': 'gender.npy',
            'glasses': 'glasses.npy',
            'height': 'height.npy',
            'width': 'width.npy',
            'black': 'race_black.npy',
            'white': 'race_white.npy',
            'yellow': 'race_yellow.npy',
            'smile': 'smile.npy',
        }
        # 属性到对应组件滑块的映射
        self.attr2slider = {
            'age': self.attr_age_slider,
            'ah': 'angle_horizontal.npy',
            'av': 'angle_vertical.npy',
            'beauty': self.attr_beauty_slider,
            'angry': self.attr_angry_slider,
            'disgust': 'emotion_disgust.npy',
            'easy': 'emotion_easy.npy',
            'fear': 'emotion_fear.npy',
            'happy': self.attr_happy_slider,
            'sad': self.attr_sad_slider,
            'surprise': self.attr_surprise_slider,
            'eyeopen': 'eyes_open.npy',
            'faceshape': 'face_shape.npy',
            'gender': self.attr_gender_slider,
            'glasses': self.attr_glasses_slider,
            'height': self.attr_height_slider,
            'width': self.attr_width_slider,
            'black': self.attr_black_slider,
            'white': self.attr_white_slider,
            'yellow': self.attr_yellow_slider,
            'smile': self.attr_smile_slider,
        }
        # 记录属性值上的变动
        self.attr_ops = {}
        # 记录以保存当前调整后的图像
        self.image = None
        # latent code（最原始的，不变动）
        self.latent = None
        # 保存图像名
        self.save_name = None
        self._connect()
        self._disable_img()
        self._disable_vid()
        self._enable_choose()
        # 控制窗口移动
        self.move_Flag = False
        self.mouse_x = self.mouse_y = self.origin_x = self.origin_y = None

    # override mouse press & move & release event to enable window movement
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.move_Flag = False
        if a0.button() == Qt.LeftButton and self.space.underMouse():
            self.setCursor(Qt.OpenHandCursor)
            # 但判断条件满足时候, 把拖动标识位设定为真
            self.move_Flag = True
            self.mouse_x = a0.globalX()
            self.mouse_y = a0.globalY()

            # 获取窗体当前坐标
            self.origin_x = self.x()
            self.origin_y = self.y()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        # 拖动标识位设定为真时, 进入移动事件
        if self.move_Flag:
            # 计算鼠标移动的x，y位移
            move_x = a0.globalX() - self.mouse_x
            move_y = a0.globalY() - self.mouse_y

            # 计算窗体更新后的坐标：更新后的坐标 = 原本的坐标 + 鼠标的位移
            dest_x = self.origin_x + move_x
            dest_y = self.origin_y + move_y

            # 移动窗体
            self.move(dest_x, dest_y)

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        # 设定鼠标为普通状态: 箭头
        self.setCursor(Qt.ArrowCursor)

    # connect func to items in ui
    def _connect(self):
        self.bt_min.clicked.connect(self.showMinimized)
        self.bt_close.clicked.connect(self.close)
        self.img_bt_generate.clicked.connect(self._generate_img)
        self.img_bt_choose.clicked.connect(self._choose_img)
        self.img_bt_save.clicked.connect(self._save_img)
        self.img_bt_back.clicked.connect(lambda: self._set_attr(zero=True))
        self.attr_age_slider.valueChanged.connect(lambda: self._edit_img('age'))
        self.attr_gender_slider.valueChanged.connect(lambda: self._edit_img('gender'))
        self.attr_beauty_slider.valueChanged.connect(lambda: self._edit_img('beauty'))
        self.attr_angry_slider.valueChanged.connect(lambda: self._edit_img('angry'))
        self.attr_happy_slider.valueChanged.connect(lambda: self._edit_img('happy'))
        self.attr_surprise_slider.valueChanged.connect(lambda: self._edit_img('surprise'))
        self.attr_sad_slider.valueChanged.connect(lambda: self._edit_img('sad'))
        self.attr_glasses_slider.valueChanged.connect(lambda: self._edit_img('glasses'))
        self.attr_height_slider.valueChanged.connect(lambda: self._edit_img('height'))
        self.attr_width_slider.valueChanged.connect(lambda: self._edit_img('width'))
        self.attr_black_slider.valueChanged.connect(lambda: self._edit_img('black'))
        self.attr_white_slider.valueChanged.connect(lambda: self._edit_img('white'))
        self.attr_yellow_slider.valueChanged.connect(lambda: self._edit_img('yellow'))
        self.attr_smile_slider.valueChanged.connect(lambda: self._edit_img('smile'))
        self.vid_bt_img.clicked.connect(self._select_img)
        self.vid_bt_vid.clicked.connect(self._select_src)
        self.vid_bt_path.clicked.connect(self._select_dir)
        self.vid_choice.activated.connect(self._select_src_c)
        self.vid_bt_help.clicked.connect(lambda: self.d.show())
        self.vid_bt_start.clicked.connect(self._generate_vid)

    # update info to command
    def update_command(self, text):
        self.command.append(text)
        QApplication.processEvents()

    # select source image and show it on self.view with reasonable scale
    def _select_img(self):
        try:
            img_path = QFileDialog.getOpenFileName(self, '选择图片', '', 'Excel files(*.jpg; *.png; *.jpeg)')
            if img_path:
                self.view.scale(1./self.scale, 1./self.scale)
                self.src_img = img_path[0]
                self.update_command("选择图像：" + self.src_img)
                # load image to pixmap and put it into scene
                im = cv2.imread(self.src_img)
                img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                y, x = im.shape[:-1]
                frame = QImage(img, x, y, QImage.Format_RGB888)
                self.scene.clear()
                pix = QPixmap.fromImage(frame)
                self.scene.addPixmap(pix)
                # scale pic
                self.scale = min(self.view.width()/x, self.view.height()/y)
                # print(self.view.width(), self.view.height())
                # print(x, y)
                self.view.scale(self.scale, self.scale)
                self._enable_vid()
                self.vid_bt_start.setDisabled(True)
                self.vid_choice.setDisabled(False)
        except:
            self.update_command("选择图像失败！")

    # choose source video by combobox
    def _select_src_c(self):
        if self.vid_choice.currentText() != '无预设':
            t = self.vid_choice.currentText()
            if t == '样例':
                self.src_vid = 'example/990.mp4'
            elif t == '周星驰':
                self.src_vid = 'example/zxc1.mp4'
            elif t == '金馆长':
                self.src_vid = 'example/jin.mp4'
            self.update_command("选择驱动视频：" + self.src_vid)
            self.vid_bt_start.setDisabled(False)

    # choose source video by push button
    def _select_src(self):
        try:
            video_path = QFileDialog.getOpenFileName(self, '选择视频', '', 'Excel files(*.mp4; *.flv; *.avi)')
            if video_path:
                self.src_vid = video_path[0]
                self.update_command("选择驱动视频：" + self.src_vid)
                self.vid_bt_start.setDisabled(False)
        except:
            self.update_command("选择驱动视频失败！")
    
    # choose save path, default ./res
    def _select_dir(self):
        try:
            dir_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
            if dir_path:
                self.vid_save_path = dir_path
                self.update_command("选择存储路径：" + self.vid_save_path)
        except:
            self.update_command("选择存储路径失败！")

    # disable components while running
    # 无效化图像编辑部分的组件
    def _disable_img(self):
        self.img_bt_generate.setDisabled(True)
        self.img_bt_choose.setDisabled(True)
        self.img_bt_save.setDisabled(True)
        self.img_bt_back.setDisabled(True)
        self.attr_age_slider.setDisabled(True)
        self.attr_gender_slider.setDisabled(True)
        self.attr_beauty_slider.setDisabled(True)
        self.attr_angry_slider.setDisabled(True)
        self.attr_happy_slider.setDisabled(True)
        self.attr_surprise_slider.setDisabled(True)
        self.attr_sad_slider.setDisabled(True)
        self.attr_glasses_slider.setDisabled(True)
        self.attr_height_slider.setDisabled(True)
        self.attr_width_slider.setDisabled(True)
        self.attr_black_slider.setDisabled(True)
        self.attr_white_slider.setDisabled(True)
        self.attr_yellow_slider.setDisabled(True)
        self.attr_smile_slider.setDisabled(True)

    # 无效化驱动视频模块的组件
    def _disable_vid(self):
        self.vid_bt_img.setDisabled(True)
        self.vid_bt_vid.setDisabled(True)
        self.vid_bt_path.setDisabled(True)
        self.vid_bt_start.setDisabled(True)
        self.vid_choice.setDisabled(True)
        self.vid_save_pic.setDisabled(True)
        self.vid_sr.setDisabled(True)

    # 启用选择相关的组件
    def _enable_choose(self):
        self.img_bt_generate.setDisabled(False)
        self.img_bt_choose.setDisabled(False)
        self.vid_bt_img.setDisabled(False)
        self.vid_bt_help.setDisabled(False)

    # 无效化选择相关的组件
    def _disable_choose(self):
        self.img_bt_generate.setDisabled(True)
        self.img_bt_choose.setDisabled(True)
        self.vid_bt_img.setDisabled(True)
        self.vid_bt_help.setDisabled(True)

    # 启用图像编辑相关的组件
    def _enable_img(self):
        self.img_bt_generate.setDisabled(False)
        self.img_bt_choose.setDisabled(False)
        self.img_bt_save.setDisabled(False)
        self.img_bt_back.setDisabled(False)
        self.attr_age_slider.setDisabled(False)
        self.attr_gender_slider.setDisabled(False)
        self.attr_beauty_slider.setDisabled(False)
        self.attr_angry_slider.setDisabled(False)
        self.attr_happy_slider.setDisabled(False)
        self.attr_surprise_slider.setDisabled(False)
        self.attr_sad_slider.setDisabled(False)
        self.attr_glasses_slider.setDisabled(False)
        self.attr_height_slider.setDisabled(False)
        self.attr_width_slider.setDisabled(False)
        self.attr_black_slider.setDisabled(False)
        self.attr_white_slider.setDisabled(False)
        self.attr_yellow_slider.setDisabled(False)
        self.attr_smile_slider.setDisabled(False)

    # 启用视频相关的组件
    def _enable_vid(self):
        self.vid_bt_img.setDisabled(False)
        self.vid_bt_vid.setDisabled(False)
        self.vid_bt_path.setDisabled(False)
        self.vid_bt_start.setDisabled(False)
        self.vid_choice.setDisabled(False)
        self.vid_save_pic.setDisabled(False)
        self.vid_sr.setDisabled(False)

    # 随机生成可编辑的图像
    def _generate_img(self):
        self._disable_img()
        self._disable_choose()
        self._set_attr(zero=True)
        self.attr_ops.clear()
        self.save_name = None
        self.image = None
        self.latent = None
        self.update_command('generating image...')
        generate_image(self)
        self.update_command(f'generating image done!')
        self._enable_choose()
        self._enable_img()

    # 保存编辑后的图像
    def _save_img(self):
        self.save_name = QFileDialog.getSaveFileName(self, '保存图像', 'res', '*.png')[0]
        self.save_name = self.save_name.split('.')[0]
        self.image.save(self.save_name + '.png')
        with open(self.save_name + '.txt', 'w') as f:
            text_save(f, self.latent)
            if self.attr_ops:
                for key in self.attr_ops.keys():
                    s = str(key) + '\n'
                    f.write(s)
                    s = str(self.attr_ops[key]) + '\n'
                    f.write(s)
        self.update_command('save image done!')

    # 选择图像进行编辑
    def _choose_img(self):
        self._disable_img()
        self._disable_choose()
        save_name = QFileDialog.getOpenFileName(self, '选择图片', '', 'Excel files(*.jpg ; *.png; *.jpeg)')[0]
        self.save_name = save_name.split('.')[0]
        if self.save_name:
            self.attr_ops.clear()
            self.image = None
            self.latent = None
            self.view.scale(1. / self.scale, 1. / self.scale)
            self.update_command("选择图像：" + self.save_name)
            # load image to pixmap and put it into scene
            im = cv2.imread(self.save_name + '.png')
            img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            y, x = im.shape[:-1]
            frame = QImage(img, x, y, QImage.Format_RGB888)
            self.scene.clear()
            pix = QPixmap.fromImage(frame)
            self.scene.addPixmap(pix)
            # scale pic
            self.scale = min(self.view.width() / x, self.view.height() / y)
            self.view.scale(self.scale, self.scale)
            self._enable_img()
            latent = read_feature(self, self.save_name + '.txt')
            self.latent = np.stack(latent for _ in range(1))
            self._enable_img()
        self._enable_choose()
        self._set_attr()

    # 设置图像对应的参数（当加载时）
    def _set_attr(self, zero=False):
        for slider_name in self.attr2slider.keys():
            if type(self.attr2slider[slider_name]) is not str:
                if zero:
                    self.attr2slider[slider_name].setValue(0)
                else:
                    if slider_name in self.attr_ops.keys():
                        self.attr2slider[slider_name].setValue(self.attr_ops[slider_name])

    # 编辑图像
    def _edit_img(self, attr):
        if self.latent is None:
            self.update_command('can\'t find latent code to edit image!')
            return
        for i in range(len(self.values)):
            value = self.sliders[i].value()
            self.values[i].setText(str(value))
        self.attr_ops.update({attr: self.attr2slider[attr].value()})
        edit_image(self)

    # generate animation via source video and pic
    def _generate_vid(self):
        if self.vid_choice.currentText() != '无预设':
            pass
        if self.src_vid and self.src_img and self.vid_save_path:
            self._disable_choose()
            self._disable_vid()
            img_full_name = os.path.split(self.src_img)[1]
            img_name = os.path.splitext(img_full_name)[0]
            source_image = self.src_img
            driving_video = self.src_vid
            result_video = os.path.join(self.vid_save_path, f'{img_name}.mp4')
            imgs_dir = os.path.join(self.vid_save_path, img_name)
            self.update_command(f'imgs_dir: {imgs_dir}')
            os.makedirs(imgs_dir, exist_ok=True)
            relative = True
            adapt_scale = True

            source_image = imageio.imread(source_image)
            reader = imageio.get_reader(driving_video)
            fps = reader.get_meta_data()['fps']
            driving_video = []
            frame_count = 0
            try:
                for im in reader:
                    driving_video.append(im)
                    frame_count += 1
                    self.update_command(f'loading frame: {frame_count} ...')
            except RuntimeError:
                pass
            reader.close()

            self.update_command('resizing to 256...')
            source_image = resize(source_image, (256, 256))[..., :3]
            driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]
            self.update_command('done!')

            self.update_command('loading checkpoints...')
            generator, kp_detector = load_checkpoints(config_path=self.vid_yaml_path,
                                                      checkpoint_path=self.vid_checkpoint, cpu=False)
            self.update_command('load checkpoints done!')

            self.update_command('start generating animation...')
            predictions = []
            self.vid_finish_flag = 0
            generate_animation(self, predictions, frame_count, source_image, driving_video, generator, kp_detector,
                               relative, adapt_scale, False)
            self.update_command('generation done!')

            self.update_command('start saving video...')
            imageio.mimsave(result_video, [img_as_ubyte(frame) for frame in predictions], fps=fps)
            self.update_command('saving video done!')
            self.img_save_flag = self.vid_save_pic.isChecked()
            if self.img_save_flag:
                self.update_command('start saving images...')
                for f in range(len(predictions)):
                    img = img_as_ubyte(predictions[f])
                    out_img_path = os.path.join(imgs_dir, f'{f}.jpg')
                    imageio.imsave(out_img_path, img)
                    self.update_command(f'save image: {out_img_path}')
            self.update_command('All Done!')
            self._enable_choose()
            self._enable_vid()
            torch.cuda.empty_cache()

    # 载入图像编辑基本模型（可以实时编辑属性）
    def model_load(self):
        self._disable_choose()
        self.update_command('loading checkpoint...')
        tflib.init_tf()
        with open('checkpoint/model.cfg', 'r')as f:
            model = f.read().strip()
        if model:
            stream = open('checkpoint/'+model, 'rb')
        else:
            stream = open('checkpoint/generator_yellow-stylegan2-config-f.pkl', 'rb')
        with stream:
            _G, _D, self.Gs = pickle.load(stream, encoding='latin1')
        stream.close()
        self.update_command('load done!')
        self._enable_choose()


class dialogUi(QDialog):
    def __init__(self, parent=None):
        super(dialogUi, self).__init__(parent)
        self.d = Ui_Dialog()
        self.d.setupUi(self)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)
        self.setAttribute(
            QtCore.Qt.WA_TranslucentBackground)

        self.d.bn_min.clicked.connect(lambda: self.showMinimized())
        self.d.bn_close.clicked.connect(lambda: self.close())
        self.dragPos = self.pos()  # INITIAL POSOTION OF THE DIALOGBOX

        def movedialogWindow(event):
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.d.frame_top.mouseMoveEvent = movedialogWindow  # CALLING THE FUNCTION TO CJANGE THE POSITION OF THE DIALOGBOX DURING MOUSE DRAG

    # ----> FUNCTION TO CAPTURE THE INITIAL POSITION OF THE MOUSE
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    ex.model_load()
    sys.exit(app.exec_())
