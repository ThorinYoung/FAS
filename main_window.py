from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# 主界面
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # styles
        self.setWindowFlags(Qt.FramelessWindowHint)
        p = self.palette()
        p.setColor(QPalette.Base, QColor('#111111'))
        p.setColor(QPalette.Window, QColor('#555555'))
        p.setColor(QPalette.WindowText, QColor('#E8E8E8'))
        p.setColor(QPalette.Text, QColor('#1C1C1C'))

        self.values = []
        self.sliders = []

        self.setPalette(p)

        self.big_font = QFont('', 20, 65)
        self.label_font = QFont('', 15, 65)
        self.mid_font = QFont('', 11, 75)

        self.normal_bt_style = '''
            QPushButton {
                border: 2px solid rgb(51,51,51);
                border-radius: 5px;    
                color:rgb(255,255,255);
                background-color: rgb(51,51,51);
            }
            QPushButton:hover {
                border: 2px solid rgb(0,143,150);
                background-color: rgb(0,143,150);
            }
            QPushButton:pressed {    
                border: 2px solid rgb(0,143,150);
                background-color: rgb(51,51,51);
            }

            QPushButton:disabled {    
                border-radius: 5px;    
                border: 2px solid rgb(112,112,112);
                background-color: rgb(112,112,112);
            }'''

        self.start_bt_style = '''
            QPushButton {
                border: 2px solid rgb(51,51,51);
                border-radius: 5px;    
                color:rgb(255,255,255);
                background-color: rgb(51,51,51);
            }
            QPushButton:hover {
                border: 5px solid rgb(0,143,150);
                background-color: rgb(0,180,180);
            }
            QPushButton:pressed {    
                border: 2px solid rgb(0,143,150);
                background-color: rgb(51,51,51);
            }

            QPushButton:disabled {    
                border-radius: 5px;    
                border: 2px solid rgb(112,112,112);
                background-color: rgb(112,112,112);
            }'''

        self.normal_slider_style = '''
            QSlider::handle:horizontal {
                width: 5px;
                border-radius: 2px;
                margin-top: 2px;
                margin-bottom: 2px;
                background-color: rgb(51,51,51);
            }
            QSlider::handle:horizontal:hover {
                background-color: rgb(0,143,150);
            }
            QSlider::handle:horizontal:pressed {    
                background-color: rgb(51,51,51);
                border: 2px solid rgb(0,143,150);
            }
            QSlider::handle:horizontal:disabled {    
                background-color: rgb(112,112,112);
            }
            '''

        self.normal_combo_style = '''
            QComboBox {
                border: 2px solid rgb(51,51,51);
                border-radius: 5px;    
                color:rgb(255,255,255);
                background-color: rgb(51,51,51);
            }
            
            QComboBox:hover {
                border: 2px solid rgb(0,143,150);
                border-radius: 5px;    
                color:rgb(255,255,255);
                background-color: rgb(0,143,150);
            }
            
            QComboBox:!editable, QComboBox::drop-down:editable {
                background: rgb(51,51,51);
            }
            
            QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                background:rgb(51,51,51);
            }
            
            QComboBox:on { /* shift the text when the popup opens */
                padding-top: 3px;
                padding-left: 4px;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;

                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* just a single line */
                border-top-right-radius: 5px; /* same radius as the QComboBox */
                border-bottom-right-radius: 5px;
            }
            
            QComboBox::down-arrow {
                image: url(assets/icon/arrow.png);
            }
            
            QComboBox::down-arrow:on { /* shift the arrow when popup is open */
                top: 1px;
                left: 1px;
            }
            
            QComboBox::drop-down {
                background:rgb(51,51,51);
            }
            
            QComboBox::drop-down:disabled {
                background:rgb(112,112,112);
            }
            
            QComboBox QAbstractItemView {
                color: white;
                background-color: rgb(54,54,54);   
                selection-background-color: rgb(0,143,150);
            }
            
            QComboBox:disabled {
                color: white;
                background-color: rgb(112,112,112);  
                border: 0px solid rgb(51,51,51);
            }
            '''

        self.normal_txtbs_style = '''
            QTextBrowser {
                background: black;
                color:white;
            }
            '''

        self.min_button_style = '''
        QPushButton {
            border: none;
            background-color: rgba(0,0,0,0);
        }
        QPushButton:hover {
            background-color: rgb(0,143,150);
        }
        QPushButton:pressed {
            background-color: rgba(0,0,0,0);
        }
        '''

        self.close_button_style = '''
        QPushButton {
            border: none;
            background-color: rgba(0,0,0,0);
        }
        QPushButton:hover {
            background-color: rgb(255,100,100);
        }
        QPushButton:pressed {
            background-color: rgba(0,0,0,0);
        }
        '''

        class MyCheckBox(QCheckBox):
            """
            基础的StyleSheet
            """

            def __init__(self, *args):
                super(MyCheckBox, self).__init__(*args)
                self.__init_style()  # 设置样式

            def __init_style(self):
                checkbox_style = '''
                QCheckBox {
                border: none;
                border-radius: 12px;
                }
                QCheckBox::indicator{
                    background-color: rgb(54,54,54);
                    border: 0px solid #b1b1b1;
                    width: 40px;
                    height: 25px;
                    border-radius: 12px;
                   }
        
                QCheckBox:enabled:checked{
                    color: rgb(255, 255, 255);
                }
                QCheckBox:enabled:!checked{
                    color: rgb(255, 255, 255);
                }
        
                QCheckBox::indicator:checked {
                        background-color: rgb(0,143,150);
                }
        
        
                QCheckBox::indicator:unchecked {
                background-color: rgb(54,54,54);
                }
                '''
                self.setStyleSheet(self.styleSheet() + checkbox_style)

            def mousePressEvent(self, *args, **kwargs):
                return super(MyCheckBox, self).mousePressEvent(*args, **kwargs)

            def mouseReleaseEvent(self, *args, **kwargs):
                return super(MyCheckBox, self).mouseReleaseEvent(*args, **kwargs)

            def paintEvent(self, pa: QPaintEvent):
                super(MyCheckBox, self).paintEvent(pa)
                if self.isChecked():
                    painter = QPainter(self)
                    painter.setPen(Qt.white)
                    painter.setBrush(Qt.white)
                    # painter.drawText(self.rect(), Qt.AlignLeft, "test")
                    painter.drawEllipse(18, 3, 18, 18)
                else:
                    painter = QPainter(self)
                    painter.setPen(Qt.white)
                    painter.setBrush(Qt.white)
                    # painter.drawText(self.rect(), Qt.AlignLeft, "test")
                    painter.drawEllipse(4, 3, 18, 18)

        self.title_font = QFont('黑体', 20, 75)
        self.normal_font = QFont('', 10, 75)

        self.setWindowTitle('人脸动画生成系统')
        self.setMaximumHeight(900)
        self.setMaximumWidth(950)
        self.move(400, 50)

        # components
        # main_layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setSpacing(18)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # title_layout
        self.title_layout = QHBoxLayout()
        self.title_layout.setAlignment(Qt.AlignRight)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(0)
        self.bt_min = QPushButton()
        self.bt_min.setFixedSize(QSize(70, 50))
        self.bt_min.setContentsMargins(0, 0, 0, 0)
        self.bt_min.setStyleSheet(self.min_button_style)
        min_icon = QIcon()
        min_icon.addPixmap(QPixmap('assets/icon/hide.png'), QIcon.Normal, QIcon.Off)
        self.bt_min.setIcon(min_icon)
        self.bt_min.setIconSize(QSize(60, 42))
        self.bt_close = QPushButton()
        self.bt_close.setFixedSize(QSize(70, 50))
        self.bt_close.setContentsMargins(0, 0, 0, 0)
        self.bt_close.setStyleSheet(self.close_button_style)
        close_icon = QIcon()
        close_icon.addPixmap(QPixmap('assets/icon/close.png'), QIcon.Normal, QIcon.Off)
        self.bt_close.setIcon(close_icon)
        self.bt_close.setIconSize(QSize(60, 42))
        self.title_box = QHBoxLayout()
        self.title_box.setAlignment(Qt.AlignLeft)
        self.title_label = QLabel()
        self.title_label.setContentsMargins(10, 10, 10, 0)
        self.title_label.setText('人脸动画生成系统')
        self.title_label.setMinimumSize(QSize(0, 40))
        self.title_label.setFont(self.title_font)
        self.title_box.addWidget(self.title_label)
        self.space = QLabel()
        self.space.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.title_layout.addLayout(self.title_box)
        self.title_layout.addWidget(self.space)
        self.title_layout.addWidget(self.bt_min)
        self.title_layout.addWidget(self.bt_close)

        # image_editing_layout
        self.img_layout = QHBoxLayout()
        self.img_layout.setAlignment(Qt.AlignLeft)
        self.img_layout_l = QVBoxLayout()
        self.img_layout_l.setAlignment(Qt.AlignTop)
        self.img_layout_r = QVBoxLayout()
        self.img_layout_r.setAlignment(Qt.AlignCenter)

        # left layout
        self.view = QGraphicsView()
        self.view.setMinimumSize(QSize(500, 500))
        self.view.setMaximumSize(QSize(700, 700))
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # buttons in one layout
        self.img_bt_layout = QHBoxLayout()
        self.img_bt_layout.setAlignment(Qt.AlignCenter)
        self.img_bt_generate = QPushButton('生成随机图像')
        self.img_bt_generate.setMinimumSize(QSize(70, 50))
        self.img_bt_generate.setMaximumSize(QSize(100, 60))
        self.img_bt_generate.setStyleSheet(self.normal_bt_style)
        self.img_bt_choose = QPushButton('选择图像')
        self.img_bt_choose.setMinimumSize(QSize(70, 50))
        self.img_bt_choose.setMaximumSize(QSize(100, 60))
        self.img_bt_choose.setStyleSheet(self.normal_bt_style)
        self.img_bt_choose.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.img_bt_save = QPushButton('另存为')
        self.img_bt_save.setMinimumSize(QSize(70, 50))
        self.img_bt_save.setMaximumSize(QSize(100, 60))
        self.img_bt_save.setStyleSheet(self.normal_bt_style)
        self.img_bt_save.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.img_bt_back = QPushButton('复位')
        self.img_bt_back.setMinimumSize(QSize(70, 50))
        self.img_bt_back.setMaximumSize(QSize(100, 60))
        self.img_bt_back.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.img_bt_back.setStyleSheet(self.normal_bt_style)
        self.img_bt_layout.addWidget(self.img_bt_generate)
        self.img_bt_layout.addWidget(self.img_bt_choose)
        self.img_bt_layout.addWidget(self.img_bt_save)
        self.img_bt_layout.addWidget(self.img_bt_back)
        self.img_layout_l.addWidget(self.view)
        self.img_layout_l.addLayout(self.img_bt_layout)

        # right layout
        # here every block stands for an attribute slider
        self.attr_age_layout = QHBoxLayout()
        self.attr_age_layout.setAlignment(Qt.AlignLeft)
        self.attr_age_label = QLabel('年龄')
        self.attr_age_slider = QSlider(Qt.Horizontal)
        self.attr_age_slider.setMinimumWidth(300)
        self.attr_age_slider.setMaximumWidth(400)
        self.attr_age_slider.setValue(0)
        self.attr_age_slider.setMinimum(-15)
        self.attr_age_slider.setMaximum(15)
        self.attr_age_slider.setStyleSheet(self.normal_slider_style)
        self.attr_age_value = QLabel()
        self.attr_age_value.setText('0')
        self.attr_age_value.setMinimumWidth(30)
        self.attr_age_layout.addWidget(self.attr_age_label)
        self.attr_age_layout.addWidget(self.attr_age_slider)
        self.attr_age_layout.addWidget(self.attr_age_value)
        self.values.append(self.attr_age_value)
        self.sliders.append(self.attr_age_slider)

        self.attr_gender_layout = QHBoxLayout()
        self.attr_gender_layout.setAlignment(Qt.AlignLeft)
        self.attr_gender_label = QLabel('性别')
        self.attr_gender_slider = QSlider(Qt.Horizontal)
        self.attr_gender_slider.setMinimumWidth(300)
        self.attr_gender_slider.setMaximumWidth(400)
        self.attr_gender_slider.setValue(0)
        self.attr_gender_slider.setMinimum(-15)
        self.attr_gender_slider.setMaximum(15)
        self.attr_gender_value = QLabel()
        self.attr_gender_value.setText('0')
        self.attr_gender_value.setMinimumWidth(30)
        self.attr_gender_slider.setStyleSheet(self.normal_slider_style)
        self.attr_gender_layout.addWidget(self.attr_gender_label)
        self.attr_gender_layout.addWidget(self.attr_gender_slider)
        self.attr_gender_layout.addWidget(self.attr_gender_value)
        self.values.append(self.attr_gender_value)
        self.sliders.append(self.attr_gender_slider)

        self.attr_beauty_layout = QHBoxLayout()
        self.attr_beauty_layout.setAlignment(Qt.AlignLeft)
        self.attr_beauty_label = QLabel('美化')
        self.attr_beauty_slider = QSlider(Qt.Horizontal)
        self.attr_beauty_slider.setMinimumWidth(300)
        self.attr_beauty_slider.setMaximumWidth(400)
        self.attr_beauty_slider.setValue(0)
        self.attr_beauty_slider.setMinimum(-15)
        self.attr_beauty_slider.setMaximum(15)
        self.attr_beauty_value = QLabel()
        self.attr_beauty_value.setText('0')
        self.attr_beauty_value.setMinimumWidth(30)
        self.attr_beauty_slider.setStyleSheet(self.normal_slider_style)
        self.attr_beauty_layout.addWidget(self.attr_beauty_label)
        self.attr_beauty_layout.addWidget(self.attr_beauty_slider)
        self.attr_beauty_layout.addWidget(self.attr_beauty_value)
        self.values.append(self.attr_beauty_value)
        self.sliders.append(self.attr_beauty_slider)

        self.attr_angry_layout = QHBoxLayout()
        self.attr_angry_layout.setAlignment(Qt.AlignLeft)
        self.attr_angry_label = QLabel('愤怒')
        self.attr_angry_slider = QSlider(Qt.Horizontal)
        self.attr_angry_slider.setMinimumWidth(300)
        self.attr_angry_slider.setMaximumWidth(400)
        self.attr_angry_slider.setValue(0)
        self.attr_angry_slider.setMinimum(-15)
        self.attr_angry_slider.setMaximum(15)
        self.attr_angry_value = QLabel()
        self.attr_angry_value.setText('0')
        self.attr_angry_value.setMinimumWidth(30)
        self.attr_angry_slider.setStyleSheet(self.normal_slider_style)
        self.attr_angry_layout.addWidget(self.attr_angry_label)
        self.attr_angry_layout.addWidget(self.attr_angry_slider)
        self.attr_angry_layout.addWidget(self.attr_angry_value)
        self.values.append(self.attr_angry_value)
        self.sliders.append(self.attr_angry_slider)

        self.attr_happy_layout = QHBoxLayout()
        self.attr_happy_layout.setAlignment(Qt.AlignLeft)
        self.attr_happy_label = QLabel('喜悦')
        self.attr_happy_slider = QSlider(Qt.Horizontal)
        self.attr_happy_slider.setMinimumWidth(300)
        self.attr_happy_slider.setMaximumWidth(400)
        self.attr_happy_slider.setValue(0)
        self.attr_happy_slider.setMinimum(-15)
        self.attr_happy_slider.setMaximum(15)
        self.attr_happy_value = QLabel()
        self.attr_happy_value.setText('0')
        self.attr_happy_value.setMinimumWidth(30)
        self.attr_happy_slider.setStyleSheet(self.normal_slider_style)
        self.attr_happy_layout.addWidget(self.attr_happy_label)
        self.attr_happy_layout.addWidget(self.attr_happy_slider)
        self.attr_happy_layout.addWidget(self.attr_happy_value)
        self.values.append(self.attr_happy_value)
        self.sliders.append(self.attr_happy_slider)

        self.attr_surprise_layout = QHBoxLayout()
        self.attr_surprise_layout.setAlignment(Qt.AlignLeft)
        self.attr_surprise_label = QLabel('惊讶')
        self.attr_surprise_slider = QSlider(Qt.Horizontal)
        self.attr_surprise_slider.setMinimumWidth(300)
        self.attr_surprise_slider.setMaximumWidth(400)
        self.attr_surprise_slider.setValue(0)
        self.attr_surprise_slider.setMinimum(-15)
        self.attr_surprise_slider.setMaximum(15)
        self.attr_surprise_value = QLabel()
        self.attr_surprise_value.setText('0')
        self.attr_surprise_value.setMinimumWidth(30)
        self.attr_surprise_slider.setStyleSheet(self.normal_slider_style)
        self.attr_surprise_layout.addWidget(self.attr_surprise_label)
        self.attr_surprise_layout.addWidget(self.attr_surprise_slider)
        self.attr_surprise_layout.addWidget(self.attr_surprise_value)
        self.values.append(self.attr_surprise_value)
        self.sliders.append(self.attr_surprise_slider)

        self.attr_sad_layout = QHBoxLayout()
        self.attr_sad_layout.setAlignment(Qt.AlignLeft)
        self.attr_sad_label = QLabel('悲伤')
        self.attr_sad_slider = QSlider(Qt.Horizontal)
        self.attr_sad_slider.setMinimumWidth(300)
        self.attr_sad_slider.setMaximumWidth(400)
        self.attr_sad_slider.setValue(0)
        self.attr_sad_slider.setMinimum(-15)
        self.attr_sad_slider.setMaximum(15)
        self.attr_sad_value = QLabel()
        self.attr_sad_value.setText('0')
        self.attr_sad_value.setMinimumWidth(30)
        self.attr_sad_slider.setStyleSheet(self.normal_slider_style)
        self.attr_sad_layout.addWidget(self.attr_sad_label)
        self.attr_sad_layout.addWidget(self.attr_sad_slider)
        self.attr_sad_layout.addWidget(self.attr_sad_value)
        self.values.append(self.attr_sad_value)
        self.sliders.append(self.attr_sad_slider)

        self.attr_glasses_layout = QHBoxLayout()
        self.attr_glasses_layout.setAlignment(Qt.AlignLeft)
        self.attr_glasses_label = QLabel('眼镜')
        self.attr_glasses_slider = QSlider(Qt.Horizontal)
        self.attr_glasses_slider.setMinimumWidth(300)
        self.attr_glasses_slider.setMaximumWidth(400)
        self.attr_glasses_slider.setValue(0)
        self.attr_glasses_slider.setMinimum(-15)
        self.attr_glasses_slider.setMaximum(15)
        self.attr_glasses_value = QLabel()
        self.attr_glasses_value.setText('0')
        self.attr_glasses_value.setMinimumWidth(30)
        self.attr_glasses_slider.setStyleSheet(self.normal_slider_style)
        self.attr_glasses_layout.addWidget(self.attr_glasses_label)
        self.attr_glasses_layout.addWidget(self.attr_glasses_slider)
        self.attr_glasses_layout.addWidget(self.attr_glasses_value)
        self.values.append(self.attr_glasses_value)
        self.sliders.append(self.attr_glasses_slider)

        self.attr_height_layout = QHBoxLayout()
        self.attr_height_layout.setAlignment(Qt.AlignLeft)
        self.attr_height_label = QLabel('高度')
        self.attr_height_slider = QSlider(Qt.Horizontal)
        self.attr_height_slider.setMinimumWidth(300)
        self.attr_height_slider.setMaximumWidth(400)
        self.attr_height_slider.setValue(0)
        self.attr_height_slider.setMinimum(-15)
        self.attr_height_slider.setMaximum(15)
        self.attr_height_value = QLabel()
        self.attr_height_value.setText('0')
        self.attr_height_value.setMinimumWidth(30)
        self.attr_height_slider.setStyleSheet(self.normal_slider_style)
        self.attr_height_layout.addWidget(self.attr_height_label)
        self.attr_height_layout.addWidget(self.attr_height_slider)
        self.attr_height_layout.addWidget(self.attr_height_value)
        self.values.append(self.attr_height_value)
        self.sliders.append(self.attr_height_slider)

        self.attr_width_layout = QHBoxLayout()
        self.attr_width_layout.setAlignment(Qt.AlignLeft)
        self.attr_width_label = QLabel('宽度')
        self.attr_width_slider = QSlider(Qt.Horizontal)
        self.attr_width_slider.setMinimumWidth(300)
        self.attr_width_slider.setMaximumWidth(400)
        self.attr_width_slider.setValue(0)
        self.attr_width_slider.setMinimum(-15)
        self.attr_width_slider.setMaximum(15)
        self.attr_width_value = QLabel()
        self.attr_width_value.setText('0')
        self.attr_width_value.setMinimumWidth(30)
        self.attr_width_slider.setStyleSheet(self.normal_slider_style)
        self.attr_width_layout.addWidget(self.attr_width_label)
        self.attr_width_layout.addWidget(self.attr_width_slider)
        self.attr_width_layout.addWidget(self.attr_width_value)
        self.values.append(self.attr_width_value)
        self.sliders.append(self.attr_width_slider)

        self.attr_black_layout = QHBoxLayout()
        self.attr_black_layout.setAlignment(Qt.AlignLeft)
        self.attr_black_label = QLabel('黑人')
        self.attr_black_slider = QSlider(Qt.Horizontal)
        self.attr_black_slider.setMinimumWidth(300)
        self.attr_black_slider.setMaximumWidth(400)
        self.attr_black_slider.setValue(0)
        self.attr_black_slider.setMinimum(-15)
        self.attr_black_slider.setMaximum(15)
        self.attr_black_value = QLabel()
        self.attr_black_value.setText('0')
        self.attr_black_value.setMinimumWidth(30)
        self.attr_black_slider.setStyleSheet(self.normal_slider_style)
        self.attr_black_layout.addWidget(self.attr_black_label)
        self.attr_black_layout.addWidget(self.attr_black_slider)
        self.attr_black_layout.addWidget(self.attr_black_value)
        self.values.append(self.attr_black_value)
        self.sliders.append(self.attr_black_slider)

        self.attr_white_layout = QHBoxLayout()
        self.attr_white_layout.setAlignment(Qt.AlignLeft)
        self.attr_white_label = QLabel('白人')
        self.attr_white_slider = QSlider(Qt.Horizontal)
        self.attr_white_slider.setMinimumWidth(300)
        self.attr_white_slider.setMaximumWidth(400)
        self.attr_white_slider.setValue(0)
        self.attr_white_slider.setMinimum(-15)
        self.attr_white_slider.setMaximum(15)
        self.attr_white_value = QLabel()
        self.attr_white_value.setText('0')
        self.attr_white_value.setMinimumWidth(30)
        self.attr_white_slider.setStyleSheet(self.normal_slider_style)
        self.attr_white_layout.addWidget(self.attr_white_label)
        self.attr_white_layout.addWidget(self.attr_white_slider)
        self.attr_white_layout.addWidget(self.attr_white_value)
        self.values.append(self.attr_white_value)
        self.sliders.append(self.attr_white_slider)

        self.attr_yellow_layout = QHBoxLayout()
        self.attr_yellow_layout.setAlignment(Qt.AlignLeft)
        self.attr_yellow_label = QLabel('黄种')
        self.attr_yellow_slider = QSlider(Qt.Horizontal)
        self.attr_yellow_slider.setMinimumWidth(300)
        self.attr_yellow_slider.setMaximumWidth(400)
        self.attr_yellow_slider.setValue(0)
        self.attr_yellow_slider.setMinimum(-15)
        self.attr_yellow_slider.setMaximum(15)
        self.attr_yellow_value = QLabel()
        self.attr_yellow_value.setText('0')
        self.attr_yellow_value.setMinimumWidth(30)
        self.attr_yellow_slider.setStyleSheet(self.normal_slider_style)
        self.attr_yellow_layout.addWidget(self.attr_yellow_label)
        self.attr_yellow_layout.addWidget(self.attr_yellow_slider)
        self.attr_yellow_layout.addWidget(self.attr_yellow_value)
        self.values.append(self.attr_yellow_value)
        self.sliders.append(self.attr_yellow_slider)

        self.attr_smile_layout = QHBoxLayout()
        self.attr_smile_layout.setAlignment(Qt.AlignLeft)
        self.attr_smile_label = QLabel('笑容')
        self.attr_smile_slider = QSlider(Qt.Horizontal)
        self.attr_smile_slider.setMinimumWidth(300)
        self.attr_smile_slider.setMaximumWidth(400)
        self.attr_smile_slider.setValue(0)
        self.attr_smile_slider.setMinimum(-15)
        self.attr_smile_slider.setMaximum(15)
        self.attr_smile_value = QLabel()
        self.attr_smile_value.setText('0')
        self.attr_smile_value.setMinimumWidth(30)
        self.attr_smile_slider.setStyleSheet(self.normal_slider_style)
        self.attr_smile_layout.addWidget(self.attr_smile_label)
        self.attr_smile_layout.addWidget(self.attr_smile_slider)
        self.attr_smile_layout.addWidget(self.attr_smile_value)
        self.values.append(self.attr_smile_value)
        self.sliders.append(self.attr_smile_slider)

        self.img_layout_r.addLayout(self.attr_age_layout)
        self.img_layout_r.addLayout(self.attr_gender_layout)
        self.img_layout_r.addLayout(self.attr_beauty_layout)
        self.img_layout_r.addLayout(self.attr_angry_layout)
        self.img_layout_r.addLayout(self.attr_happy_layout)
        self.img_layout_r.addLayout(self.attr_surprise_layout)
        self.img_layout_r.addLayout(self.attr_sad_layout)
        self.img_layout_r.addLayout(self.attr_glasses_layout)
        self.img_layout_r.addLayout(self.attr_height_layout)
        self.img_layout_r.addLayout(self.attr_width_layout)
        self.img_layout_r.addLayout(self.attr_black_layout)
        self.img_layout_r.addLayout(self.attr_white_layout)
        self.img_layout_r.addLayout(self.attr_yellow_layout)
        self.img_layout_r.addLayout(self.attr_smile_layout)

        self.img_layout.addLayout(self.img_layout_l)
        self.img_layout.addLayout(self.img_layout_r)

        # video_layout
        self.vid_layout = QHBoxLayout()
        self.vid_layout.setAlignment(Qt.AlignCenter)

        # video buttons
        self.vid_bt_layout = QVBoxLayout()
        self.vid_bt_layout.setAlignment(Qt.AlignCenter)
        self.vid_bt_img = QPushButton('选择图像')
        self.vid_bt_img.setMinimumSize(QSize(100, 50))
        self.vid_bt_img.setMaximumSize(QSize(130, 60))
        self.vid_bt_img.setStyleSheet(self.normal_bt_style)
        self.vid_bt_img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vid_bt_vid = QPushButton('选择驱动视频')
        self.vid_bt_vid.setMinimumSize(QSize(100, 50))
        self.vid_bt_vid.setMaximumSize(QSize(130, 60))
        self.vid_bt_vid.setStyleSheet(self.normal_bt_style)
        self.vid_bt_vid.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vid_bt_path = QPushButton('选择存储路径')
        self.vid_bt_path.setMinimumSize(QSize(100, 50))
        self.vid_bt_path.setMaximumSize(QSize(130, 60))
        self.vid_bt_path.setStyleSheet(self.normal_bt_style)
        self.vid_bt_path.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vid_bt_layout.addWidget(self.vid_bt_img)
        self.vid_bt_layout.addWidget(self.vid_bt_vid)
        self.vid_bt_layout.addWidget(self.vid_bt_path)

        # video configs
        self.vid_cfg_layout = QVBoxLayout()
        self.vid_cfg_layout.setAlignment(Qt.AlignCenter)
        self.vid_choice = QComboBox()
        self.vid_choice.addItems(['无预设', '样例', '周星驰', '金馆长'])
        self.vid_choice.setMinimumSize(QSize(100, 30))
        self.vid_choice.setStyleSheet(self.normal_combo_style)
        self.vid_save_pic = MyCheckBox('同时保存图像')
        self.vid_sr = MyCheckBox('超分辨率')
        self.vid_cfg_layout.addWidget(self.vid_choice)
        self.vid_cfg_layout.addWidget(self.vid_save_pic)
        self.vid_cfg_layout.addWidget(self.vid_sr)

        # help and start
        self.vid_hs_layout = QVBoxLayout()
        self.vid_hs_layout.setAlignment(Qt.AlignCenter)
        self.vid_bt_help = QPushButton('帮助')
        self.vid_bt_help.setMinimumSize(QSize(100, 50))
        self.vid_bt_help.setMaximumSize(QSize(130, 60))
        self.vid_bt_help.setStyleSheet(self.normal_bt_style)
        self.vid_bt_help.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vid_bt_start = QPushButton('开始！')
        self.vid_bt_start.setMinimumSize(QSize(100, 100))
        self.vid_bt_start.setMaximumSize(QSize(130, 130))
        self.vid_bt_start.setStyleSheet(self.start_bt_style)
        self.vid_bt_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vid_hs_layout.addWidget(self.vid_bt_help)
        self.vid_hs_layout.addWidget(self.vid_bt_start)

        # command line
        self.command = QTextBrowser()
        self.command.setMinimumSize(QSize(400, 200))
        self.command.setMaximumSize(QSize(400, 300))
        self.command.setStyleSheet(self.normal_txtbs_style)
        self.command.append('欢迎使用！')

        self.vid_layout.addLayout(self.vid_bt_layout)
        self.vid_layout.addLayout(self.vid_cfg_layout)
        self.vid_layout.addLayout(self.vid_hs_layout)
        self.vid_layout.addWidget(self.command)

        # add to main layout
        self.main_layout.addLayout(self.title_layout)
        self.img_layout.setContentsMargins(10, 0, 0, 0)
        self.main_layout.addLayout(self.img_layout)
        self.hline = QFrame()
        self.hline.setFrameShape(QFrame.HLine)
        self.main_layout.addWidget(self.hline)
        self.vid_layout.setContentsMargins(10, 0, 10, 10)
        self.main_layout.addLayout(self.vid_layout)

        self.main_layout.minimumSize()
        self.setLayout(self.main_layout)


# 对话框
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.normal_font = QFont('', 10, 75)
        self.normal_bt_style = '''
            QPushButton {
                border: 2px solid rgb(51,51,51);
                border-radius: 5px;    
                color:rgb(255,255,255);
                background-color: rgb(51,51,51);
            }
            QPushButton:hover {
                border: 2px solid rgb(0,143,150);
                background-color: rgb(0,143,150);
            }
            QPushButton:pressed {    
                border: 2px solid rgb(0,143,150);
                background-color: rgb(51,51,51);
            }

            QPushButton:disabled {    
                border-radius: 5px;    
                border: 2px solid rgb(112,112,112);
                background-color: rgb(112,112,112);
            }'''
        self.min_button_style = '''
        QPushButton {
            border: none;
            background-color: rgba(0,0,0,0);
        }
        QPushButton:hover {
            background-color: rgb(0,143,150);
        }
        QPushButton:pressed {
            background-color: rgba(0,0,0,0);
        }
        '''

        self.close_button_style = '''
        QPushButton {
            border: none;
            background-color: rgba(0,0,0,0);
        }
        QPushButton:hover {
            background-color: rgb(255,100,100);
        }
        QPushButton:pressed {
            background-color: rgba(0,0,0,0);
        }
        '''
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 235)
        Dialog.setMinimumSize(QtCore.QSize(450, 235))
        Dialog.setMaximumSize(QtCore.QSize(450, 235))
        Dialog.setStyleSheet("QDialog {\n"
                             "    background:rgb(51,51,51);\n"
                             "}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setStyleSheet("background:rgb(51,51,51);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_top = QtWidgets.QFrame(self.frame_2)
        self.frame_top.setMinimumSize(QtCore.QSize(0, 55))
        self.frame_top.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_top.setStyleSheet("background:rgb(91,90,90);")
        self.frame_top.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_top)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lab_heading = QtWidgets.QLabel(self.frame_top)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.lab_heading.setFont(font)
        self.lab_heading.setStyleSheet("color:rgb(255,255,255);")
        self.lab_heading.setTextFormat(QtCore.Qt.AutoText)
        self.lab_heading.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lab_heading.setObjectName("lab_heading")
        self.horizontalLayout.addWidget(self.lab_heading)
        self.bn_min = QtWidgets.QPushButton(self.frame_top)
        self.bn_min.setMinimumSize(QtCore.QSize(55, 55))
        self.bn_min.setMaximumSize(QtCore.QSize(55, 55))
        self.bn_min.setStyleSheet(self.min_button_style)
        self.bn_min.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/icon/hide.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bn_min.setIcon(icon)
        self.bn_min.setIconSize(QtCore.QSize(22, 12))
        self.bn_min.setAutoDefault(False)
        self.bn_min.setFlat(True)
        self.bn_min.setObjectName("bn_min")
        self.horizontalLayout.addWidget(self.bn_min)
        self.bn_close = QtWidgets.QPushButton(self.frame_top)
        self.bn_close.setMinimumSize(QtCore.QSize(55, 55))
        self.bn_close.setMaximumSize(QtCore.QSize(55, 55))
        self.bn_close.setStyleSheet(self.close_button_style)
        self.bn_close.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/icon/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bn_close.setIcon(icon1)
        self.bn_close.setIconSize(QtCore.QSize(22, 22))
        self.bn_close.setAutoDefault(False)
        self.bn_close.setFlat(True)
        self.bn_close.setObjectName("bn_close")
        self.horizontalLayout.addWidget(self.bn_close)
        self.verticalLayout_2.addWidget(self.frame_top)
        self.frame_bottom = QtWidgets.QFrame(self.frame_2)
        self.frame_bottom.setStyleSheet("background:rgb(91,90,90);")
        self.frame_bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom.setObjectName("frame_bottom")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_bottom)
        self.gridLayout.setObjectName("gridLayout")
        self.text = QtWidgets.QLabel(self.frame_bottom)
        self.text.setMaximumSize(QtCore.QSize(16777215, 500))
        self.text.setFont(self.normal_font)
        self.text.setStyleSheet("color:rgb(255,255,255);")
        self.text.setObjectName("text")
        self.gridLayout.addWidget(self.text)
        self.verticalLayout_2.addWidget(self.frame_bottom)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "帮助"))
        self.lab_heading.setText(_translate("Dialog", "帮助"))
        self.text.setText(_translate("Dialog", "显存不达到6G，建议一次仅使用其中一个功能\n\n*属性编辑：生成人脸或选择已生成的对象进行编辑\n\n*动画生成：选择人脸图像和人脸驱动视频进行生成，\n          可参考test4crop中的内容对任意视频截\n          取人脸部分\n"))

