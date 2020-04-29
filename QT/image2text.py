import os
import sys

import keyboard
import pyperclip
from PIL.ImageGrab import grabclipboard
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QVBoxLayout, QTextEdit, QPushButton, QMessageBox, QSystemTrayIcon, QMenu, QCheckBox
from aip import AipOcr


class Image2Text(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.keyFuck = False
        self.mousepressFuck = False

    def initUI(self):
        self.setWindowTitle("文字识别")
        layout = QVBoxLayout(self)
        self.btn1 = QRadioButton("取消换行")
        self.btn1.setChecked(True)
        self.btn2 = QRadioButton("保留换行")
        self.btn3 = QPushButton("识别")
        self.btn4 = QPushButton("截屏")
        self.btn5 = QPushButton("最小化")
        self.btn6 = QCheckBox("识别消息通知")
        self.btn6.setChecked(True)
        self.textShow = QTextEdit("先点击截屏，后点击识别")
        self.textShow.setReadOnly(True)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn6)
        layout.addWidget(self.btn4)
        layout.addWidget(self.btn3)
        layout.addWidget(self.btn5)

        self.btn3.clicked.connect(self.imageDetect)
        self.btn5.clicked.connect(self.toSys)
        self.btn4.clicked.connect(lambda: self.screenShot(layout))
        layout.addWidget(self.textShow)
        self.grabKeyboard()
        self.setMinimumSize(500, 400)
        # print(self.btn1.isChecked())
        # print(self.btn2.isChecked())

    def imageDetect(self):

        APP_ID = '11538030'
        API_KEY = 'qFXoApbGYFpeNUgRrVhHFBz6'
        SECRET_KEY = 'dzA3hD7CgQ6529uYuwlqV448MOYCq7Bf'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        try:
            image = grabclipboard()
            image.save("image.jpg")
            # image_ = image.tobitmap()
            with open("image.jpg", "rb") as f:
                image = f.read()
            response = client.basicGeneral(image)
            os.remove("image.jpg")
            if self.btn1.isChecked():
                words = ''.join(i["words"] for i in response["words_result"])
            else:
                words = '\n'.join(i["words"] for i in response["words_result"])
            self.textShow.setPlainText(words)
            pyperclip.copy(words)
            if self.isHidden() and self.btn6.isChecked():
                self.sysIcon.showMessage("已复制到剪切板", words)
        except:
            QMessageBox.about(self, "错误", "请重新截屏")

    def screenShot(self, layout):

        # layout.removeWidget(self.btn4)
        # self.textShow.grabKeyboard()
        keyboard.press(hotkey="shift+win+s")
        keyboard.release(hotkey="shift+win+s")

    def toSys(self):
        self.hide()
        self.sysIcon = QSystemTrayIcon(QIcon(QPixmap(r"C:\Users\TZK\Desktop\MFiles\body_test.png")))
        self.sysIcon.show()
        menu = QMenu()
        fuckAction = menu.addAction("显示主窗口")
        quitAction = menu.addAction("退出")
        shotAction = menu.addAction("截屏")
        detectAction = menu.addAction("识别")
        self.sysIcon.setContextMenu(menu)

        fuckAction.triggered.connect(self.show)
        quitAction.triggered.connect(self.close)
        shotAction.triggered.connect(self.screenShot)
        detectAction.triggered.connect(self.imageDetect)

        self.sysIcon.messageClicked.connect(self.show)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    main = Image2Text()
    main.show()
    sys.exit(app.exec_())