from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap
import sys

class DialogDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("对话框")
        self.btn = QPushButton("dialog", self)
        self.btn2 = QPushButton("加载文本", self)
        self.imageLabel = QLabel()
        self.textLine = QTextEdit("显示文本")
        layout = QVBoxLayout(self)
        layout.addWidget(self.btn)
        layout.addWidget(self.imageLabel)
        layout.addWidget(self.btn2)
        layout.addWidget(self.textLine)
        self.btn.clicked.connect(self.loadImage)
        self.btn2.clicked.connect(self.loadText)

    def dialogShow(self):
        dia = QDialog(self)
        dia_btn = QPushButton("nihao", dia)
        dia_btn.setWindowTitle("hellow")
        dia_btn.move(50, 50)
        dia_btn.clicked.connect(lambda: self.dia_btn_statue(dia))
        dia.exec()


    def dia_btn_statue(self, dia):
        print(self.sender().text())
        dia.close()

    def loadImage(self):
        f_path, _ = QFileDialog.getOpenFileName(self, "loadImage", '.', '(*.jpg *.png)')
        self.imageLabel.setPixmap(QPixmap(f_path))

    def loadText(self):
        f_path, _ = QFileDialog.getOpenFileName(self, "openText", "/", "(*.py *.txt)")
        with open(f_path, "r") as f:
            text = f.read()
        self.textLine.setPlainText(text)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = DialogDemo()
    w.show()
    sys.exit(app.exec_())
