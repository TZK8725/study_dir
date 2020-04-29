import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFormLayout, QLineEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator



class Validator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle("验证器")
        formlayout = QFormLayout(self)
        int_line = QLineEdit()
        double_line = QLineEdit()

        int_line.setPlaceholderText("int")

        # formlayout.addWidget(int_line)
        # formlayout.addWidget(double_line)

        formlayout.addRow("整型", int_line)
        formlayout.addRow("浮点型", double_line)

        double_line.setPlaceholderText("float")
        double_line.setEchoMode(QLineEdit.Password)

        int_val = QIntValidator()
        int_val.setRange(0, 100)
        double_val = QDoubleValidator(double_line)

        int_line.setValidator(int_val)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = Validator()
    w.show()
    sys.exit(app.exec_())