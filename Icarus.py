import os
import random
import sys
import time

from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class PetIcarus(QWidget):
    def __init__(self, parent=None):
        super(PetIcarus, self).__init__(parent)
        self.window_init()  # 初始化窗体
        self.pall_init()  # 初始化小托盘
        self.icarus_init()  # 初始化实体
        self.action_set()  # 初始化欢迎

    # 窗体初始化参数
    def window_init(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)  # 无框 | 置顶 | 子集
        self.setAutoFillBackground(False)  # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 窗口透明
        self.repaint()  # 刷新并重载

    # 非置顶窗口
    def window_widget(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget | Qt.SubWindow)  # 无框 | 标准 | 子集
        self.setAutoFillBackground(False)  # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 窗口透明
        self.repaint()  # 刷新并重载

    # 托盘化设置初始化
    def pall_init(self):
        icons = os.path.join('resource/vision/pic/Icuras.png')  # 托盘图标
        self.check_icon = os.path.join('resource/vision/pic/rcd-check.png')  # 选中图标

        self.quit_pet = QAction('退出', self)  # 退出
        self.show_set = QAction(QIcon(self.check_icon), '显示', self)  # 显示控制
        self.music_set = QAction(QIcon(self.check_icon), '声音', self)  # 声音控制
        self.text_set = QAction(QIcon(self.check_icon), '发言', self)  # 文本控制
        self.top_set = QAction(QIcon(self.check_icon), '置顶', self)  # 置顶控制
        self.about_set = QAction('关于', self)  # 详细信息

        # 菜单响应
        self.quit_pet.triggered.connect(self.quit)
        self.show_set.triggered.connect(self.show_if)
        self.music_set.triggered.connect(self.music_if)
        self.text_set.triggered.connect(self.text_if)
        self.top_set.triggered.connect(self.top_if)
        self.about_set.triggered.connect(self.about)

        # 状态判定值
        self.show_check = self.music_check = self.text_check = self.top_check = 1

        # 创建托盘菜单
        self.tray_menu = QMenu(self)

        # 添加菜单
        self.tray_menu.addAction(self.quit_pet)
        self.tray_menu.addAction(self.show_set)
        self.tray_menu.addAction(self.music_set)
        self.tray_menu.addAction(self.text_set)
        self.tray_menu.addAction(self.top_set)
        self.tray_menu.addAction(self.about_set)

        tray_icon = QSystemTrayIcon(self)  # 添加托盘图标
        tray_icon.setIcon(QIcon(icons))  # 托盘化图标
        tray_icon.setContextMenu(self.tray_menu)  # 托盘化菜单
        tray_icon.show()  # 托盘展示

    # 实体初始化
    def icarus_init(self):
        self.sentences = QLabel(self)  # 文本框定义
        self.sentences.setGeometry(0, 0, 200, 50)  # 文本框尺寸
        self.sentences.setStyleSheet("font-size:15px;font-family:微软雅黑;color:white;")  # 文本框样式
        self.sentences.setWordWrap(True)  # 自动换行

        self.pet_area = QLabel(self)  # 角色展示区域
        self.pet_area.setGeometry(0, 60, 200, 200)  # 区域尺寸
        self.pet_area.setAlignment(Qt.AlignCenter)  # 内容居中

        self.resize(200, 300)  # 定义窗体尺寸
        self.position_init()  # 定义位置
        self.show()  # 展示

        self.animate = []  # 存放动作
        for i in os.listdir("resource/vision/action"):
            self.animate.append("resource/vision/action/" + i)  # 读取动作文件

        self.dialog = []  # 存放发言
        with open("data/dialog.txt", "r") as f:
            text = f.read()  # 读取发言内容
            self.dialog = text.split("\n")  # 换行存放

    # 实体初始行为
    def action_set(self):
        self.first_timer = QTimer()  # 创建开屏动画定时器
        self.first_timer.timeout.connect(self.action_switch)  # 开屏结束
        self.first_timer.timeout.connect(self.talk_switch)  # 欢迎结束
        self.first_timer.start(5000)  # 切换计时

        self.movie = QMovie("resource/vision/interact/welcome.gif")  # 开屏动画
        self.movie.setScaledSize(QSize(200, 200))  # 动画尺寸
        self.pet_area.setMovie(self.movie)  # 加载动画
        self.movie.start()  # 播放动画
        self.welcome()  # 欢迎语录

        self.main_mod = 1  # 开屏状态设置
        self.talk_mod = 1  # 欢迎状态设置

    # 开场白
    def welcome(self):
        now_hour = time.localtime().tm_hour
        master = '主脑的打工仔~'
        if 1 <= now_hour < 3:
            self.sentences.setText('午夜好，' + master + '早点睡吧，你倒下了就没人给主脑打工了！')
        elif 3 <= now_hour < 5:
            self.sentences.setText('凌晨好，' + master + '准备享受充实的25小时吗？')
        elif 5 <= now_hour < 8:
            self.sentences.setText('早晨好，' + master + '')
        elif 8 <= now_hour < 11:
            self.sentences.setText('上午好，' + master + '')
        elif 11 <= now_hour < 13:
            self.sentences.setText('中午好，' + master + '午饭吃了吗？吃饱才有力气干活！')
        elif 13 <= now_hour < 17:
            self.sentences.setText('下午好，' + master + '')
        elif 17 <= now_hour < 19:
            self.sentences.setText('傍晚好，' + master + '')
        elif 19 <= now_hour < 23:
            self.sentences.setText('晚上好，' + master + '')
        else:
            self.sentences.setText('深夜好，' + master + '')

    # 实体待机行为
    def action_wait(self):
        self.main_timer.timeout.connect(self.action_switch)  # 待机结束执行
        self.main_timer.start(5000)  # 待机时长

        self.movie = QMovie("resource/vision/interact/state.gif")  # 开屏动画
        self.movie.setScaledSize(QSize(200, 200))  # 动画尺寸
        self.pet_area.setMovie(self.movie)  # 加载动画
        self.movie.start()  # 播放动画

        self.main_mod = 0  # 待机状态设置

    # 中场小动作
    def action_play(self):
        self.main_timer.stop()  # 结束待机状态
        self.action_timer.timeout.connect(self.action_switch)  # 小动作结束执行
        self.action_timer.start(5000)  # 小动作时长

        self.movie = QMovie(random.choice(self.animate))  # 随机加载动画
        self.movie.setScaledSize(QSize(200, 200))  # 动画尺寸
        self.pet_area.setMovie(self.movie)  # 加载动画
        self.movie.start()  # 播放动画

        self.main_mod = 2  # 小动作状态

    # 鼠标进入动作
    def action_hover(self):
        if self.main_mod != 1:
            self.main_timer.stop()  # 结束待机状态
            self.action_timer.stop()  # 结束小动作状态

            self.movie = QMovie("resource/vision/interact/hover.gif")  # 加载交互动画
            self.movie.setScaledSize(QSize(200, 200))  # 动画尺寸
            self.pet_area.setMovie(self.movie)  # 加载动画
            self.movie.start()  # 播放动画

    # 点击动作
    def action_click(self):
        self.main_timer.stop()  # 结束待机状态
        self.action_timer.stop()  # 结束小动作状态

        self.movie = QMovie("resource/vision/interact/click.gif")  # 加载点击动画
        self.movie.setScaledSize(QSize(200, 200))  # 动画尺寸
        self.pet_area.setMovie(self.movie)  # 加载动画
        self.movie.start()  # 播放动画

        self.left_mod = self.right_mod = 0

    # 动作切换
    def action_switch(self):
        if not self.main_mod:  # 待机状态判定
            self.action_play()  # 加载小动作
        elif self.main_mod:  # 开屏状态判定
            self.first_timer.stop()  # 结束开屏状态
            self.main_timer = QTimer()  # 创建主定时器
            self.action_timer = QTimer()  # 创建行为定时器
            self.action_wait()  # 待机画面
        elif self.main_mod == 2:  # 小动作状态判定
            self.action_timer.stop()  # 结束小动作
            self.action_wait()  # 待机画面

    # 待机沉默
    def talk_wait(self):
        self.quilt_timer.timeout.connect(self.talk_switch)  # 定时执行
        self.quilt_timer.start(int(random.uniform(1.2, 1.8) * 1000))  # 沉默计时

        self.sentences.setText('')  # 沉默

        self.talk_mod = 0  # 沉默状态设置

    # 待机发言
    def talk_play(self):
        self.quilt_timer.stop()  # 结束沉默状态
        self.talk_timer.timeout.connect(self.talk_switch)  # 骚话结束执行
        self.talk_timer.start(5000)  # 骚话计时

        self.sentences.setText(random.choice(self.dialog))  # 随机加载骚话

        self.talk_mod = 2  # 骚话状态设置

    # 点击发言
    def talk_click(self):
        self.quilt_timer.stop()  # 结束沉默状态
        self.talk_timer.stop()  # 结束骚话状态

        self.sentences.setText('低空飞行')

    # 发言切换
    def talk_switch(self):
        if not self.talk_mod:  # 沉默状态判定
            self.talk_play()
            # self.sentences.adjustSize()
        elif self.talk_mod:  # 欢迎状态判定
            self.quilt_timer = QTimer()  # 创建沉默计时器
            self.talk_timer = QTimer()  # 创建骚话计时器
            self.talk_wait()  # 待机沉默
        elif self.talk_mod == 2:  # 骚话判定
            self.talk_timer.stop()  # 结束骚话
            self.talk_wait()  # 待机沉默

    # 飞行音乐
    def music_fly(self):
        self.flying = QSound("resource/audio/sfx-fly-atmos.wav")
        self.flying.setLoops(QSound.Infinite)
        self.flying.play()

    # 点击音乐
    def music_click(self):
        self.fly_star_music = QSound("resource/audio/sfx-fly-start.wav")
        self.fly_star_words = QSoundEffect()
        self.fly_star_words.setSource(QUrl.fromLocalFile("resource/audio/fly-mode-zh.wav"))
        # self.fly_star_words.setVolume(1.0)
        self.fly_star_music.play()
        self.fly_star_words.play()
        QTimer.singleShot(500, self.music_fly)

    # 退出程序
    def quit(self):
        self.tray_menu.deleteLater()  # 回收托盘图标
        self.close()  # 关闭窗体
        sys.exit()  # 结束程序

    # 显示控制
    def show_if(self):
        if self.show_check:
            self.setWindowOpacity(0)
            self.show_set.setIcon(QIcon())
            self.music_set.setDisabled(True)
            self.text_set.setDisabled(True)
            self.show_check = 0
        else:
            self.setWindowOpacity(1)
            self.show_set.setIcon(QIcon(self.check_icon))
            self.music_set.setDisabled(False)
            self.text_set.setDisabled(False)
            self.show_check = 1

    def music_if(self):
        pass

    # 文本控制
    def text_if(self):
        if self.text_check:
            self.sentences.setVisible(False)
            self.text_set.setIcon(QIcon())
            self.text_check = 0
        else:
            self.sentences.setVisible(True)
            self.text_set.setIcon(QIcon(self.check_icon))
            self.text_check = 1

    def about(self):
        self.message_box('作者', '看客之眼')

    # 置顶控制
    def top_if(self):
        if self.top_check:
            self.window_widget()
            self.top_set.setIcon(QIcon())
            self.top_check = 0
        else:
            self.window_init()
            self.top_set.setIcon(QIcon(self.check_icon))
            self.top_check = 1
        self.show()

    # 初始位置
    def position_init(self):
        screen_geo = QDesktopWidget().screenGeometry()  # 获取屏幕几何
        x_pos = (screen_geo.width() - 220)  # 设置X轴
        y_pos = (screen_geo.height() - 320)  # 设置Y轴
        self.move(int(x_pos), int(y_pos))  # 定位生成

    def message_box(self, title, message):
        QMessageBox.about(self, title, message)

    # 鼠标左键事件
    def mousePressEvent(self, event):
        if self.main_mod != 1:
            if event.button() == Qt.LeftButton:
                self.action_click()
                self.talk_click()
                self.music_click()
                self.grab_all = True
            # globalPos() 事件触发点相对于桌面的位置
            # pos() 程序相对于桌面左上角的位置，实际是窗口的左上角坐标
            self.mouse_drag_pos = event.globalPos() - self.pos()  #
            event.accept()
            self.setCursor(Qt.ClosedHandCursor)  # 拖动时鼠标图形的设置

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.main_mod != 1:
            if Qt.LeftButton and self.grab_all:  # 左键与绑定判定
                old_x = self.pos().x()
                self.move(event.globalPos() - self.mouse_drag_pos)  # 移动坐标绑定
                if old_x - self.pos().x() < 0:
                    if not self.right_mod:
                        self.movie = QMovie("resource/vision/interact/right.gif")  # 加载点击动画
                        self.movie.setScaledSize(QSize(200, 200))  # 动画尺寸
                        self.pet_area.setMovie(self.movie)  # 加载动画
                        self.movie.start()  # 播放动画
                        self.right_mod = 1  # 开启右飞模式
                        self.left_mod = 0  # 关闭左飞模式
                else:
                    if not self.left_mod:
                        self.movie = QMovie("resource/vision/interact/left.gif")  # 加载点击动画
                        self.movie.setScaledSize(QSize(200, 200))  # 动画尺寸
                        self.pet_area.setMovie(self.movie)  # 加载动画
                        self.movie.start()  # 播放动画
                        self.left_mod = 1  # 开启左飞模式
                        self.right_mod = 0  # 关闭右飞模式
            event.accept()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        if self.main_mod != 1:
            self.grab_all = False
            self.action_wait()
            self.talk_wait()
        self.left_mod = self.right_mod = 0  # 关闭飞行模式
        self.setCursor(QCursor(Qt.OpenHandCursor))  # 手形鼠标

    # 鼠标进入事件
    def enterEvent(self, event):
        self.action_hover()  # 执行进入状态
        self.setCursor(QCursor(Qt.OpenHandCursor))  # 手形鼠标

    # 鼠标离开事件
    def leaveEvent(self, event):
        if self.main_mod != 1:
            self.action_wait()  # 回到待机状态

    # 鼠标右键事件
    def contextMenuEvent(self, event):
        self.tray_menu.exec_(self.mapToGlobal(event.pos()))  # 获取坐标并生成菜单


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 实例化程序
    pet = PetIcarus()  # 初始化窗口
    sys.exit(app.exec_())  # 循环直至关闭
