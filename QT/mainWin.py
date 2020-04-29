import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout, QWidget, QMenuBar,\
    QMenu, QToolBar

class mainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        self.button = QPushButton("你好")
        self.button.setToolTip("这是一个按钮")
        self.button.clicked.connect(self.close)
        # self.menu_bar = QMenuBar(self)
        # self.menu_bar.addMenu("open")
        # self.menu_bar.addMenu("New")
        self.menu = QToolBar("file", self)
        self.menu.addAction("New")
        vbox = QVBoxLayout(self)
        
        
        # vbox.addWidget(self.menu_bar)
        vbox.addWidget(self.button)
        self.resize(600, 500)
        self.setLayout(vbox)
        self.setWindowTitle("test")
        


if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = mainWindow()
    w.show()
    sys.exit(app.exec_())