from fbs_runtime.application_context.PyQt5 import ApplicationContext
import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QFileDialog, QLineEdit, QComboBox, QFormLayout, QMessageBox, QCheckBox, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize


class NewFoldGen(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.imagePathList = list()

    def initUI(self):

        self.setWindowTitle("文件夹生成器")
        self.genButton = QPushButton("生成")
        self.genButton.setToolTip("回车键")
        self.fileButton = QPushButton("打开文件目录(村名)")
        self.dangerEdit = QComboBox()
        self.dangerEdit.setToolTip("快捷键:\nB: ctrl + B\nC: ctrl + shift + C\nD: ctrl + D")
        self.nameEdit = QLineEdit()
        self.doorEdit = QLineEdit()
        self.doorEdit.setPlaceholderText("无门牌号请直接放空")
        self.fileEdit = QLineEdit()
        self.imageEdit = QLineEdit()
        self.imageButton = QPushButton("选择要复制的照片(多选)")
        self.imageButton.setToolTip("快捷键：ctrl + O")
        self.fileEdit.setPlaceholderText("村名所在目录")
        self.structureEdit = QComboBox()
        self.dangerEdit.addItems(["B", "C", "D", "A"])
        self.structureEdit.addItems(["砖混结构", "石结构", "砖木结构", "土木结构", "钢结构", "框架结构"])
        self.structureEdit.setToolTip("快捷键:\n砖混结构: ctrl + H(混)\n石结构: ctrl + shift + S(石)\n土木结构: ctrl + M(木)")
        self.delImageCheck = QCheckBox("复制完后自动删除文件夹图片(请先备份原图片)")

        formL = QFormLayout(self)
        formL.addWidget(self.fileButton)
        formL.addRow("村名所在目录", self.fileEdit)
        formL.addRow("房屋结构", self.structureEdit)
        formL.addRow("户主姓名", self.nameEdit)
        formL.addRow("门牌号", self.doorEdit)
        formL.addRow("危险等级", self.dangerEdit)

        formL.addWidget(self.imageButton)
        formL.addRow("已选择照片", self.imageEdit)
        # formL.addWidget(self.graph1)
        formL.addWidget(self.delImageCheck)
        formL.addWidget(self.genButton)
        self.setFont(QFont("MSYHL", 10))

        self.genButton.clicked.connect(self.foldGen)
        self.imageButton.clicked.connect(self.getImagePath)
        self.fileButton.clicked.connect(self.getFilePath)

    def foldGen(self):

        if len(self.nameEdit.text()) > 1:

            if len(self.doorEdit.text()) == 0:
                door_id = "无门牌号"
            else:
                door_id = self.doorEdit.text() + "号"
            danger_grade = self.dangerEdit.currentText()
            name = self.nameEdit.text()

            structure = self.structureEdit.currentText()
            fordName = " ".join([danger_grade, name, door_id, structure])
            if len(self.imagePathList):
                new_fold = self.dirPath + "/" + fordName
                os.mkdir(new_fold)
                for i in self.imagePathList:
                    file_name = i.split("/")[-1]
                    shutil.copy2(i, new_fold + "/" + file_name)
                    if self.delImageCheck.isChecked():
                        os.remove(i)
                # image_len = len(self.imagePathList)
                # self.imagePathList = None
                self.imageEdit.setText("导入完成")
                self.doorEdit.clear()
                self.nameEdit.setText(name[0])
                self.nameEdit.setFocus()
                self.imagePathList = []
            else:
                # QMessageBox.about(self, "错误", "请选择照片")
                self.getImagePath()

        else:
            QMessageBox.about(self, "错误", "请完善信息")
            self.nameEdit.setFocus()
            # QMessageBox.about("完成", "已复制{}张照片".format(image_len))

    def getImagePath(self):

        imageDialog = QFileDialog(self, "选择多张图片")
        self.imagePathList, _ = imageDialog.getOpenFileNames()
        self.imageEdit.setText("选中%d个图片"%len(self.imagePathList))
        


    def getFilePath(self):
        fileDialog = QFileDialog(self, "选择村名目录", "..")
        self.dirPath = fileDialog.getExistingDirectory()
        self.fileEdit.setText(self.dirPath)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.foldGen()
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_O:
            self.getImagePath()
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_H:
            self.structureEdit.setCurrentIndex(0)
            self.dangerEdit.setCurrentIndex(0)
        if event.modifiers() == Qt.ControlModifier|Qt.ShiftModifier and event.key() == Qt.Key_S:
            self.structureEdit.setCurrentIndex(1)
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_M:
            self.structureEdit.setCurrentIndex(3)
            self.dangerEdit.setCurrentIndex(1)
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_B:
            self.dangerEdit.setCurrentIndex(0)
        if event.modifiers() == Qt.ControlModifier|Qt.ShiftModifier and event.key() == Qt.Key_C:
            self.dangerEdit.setCurrentIndex(1)
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_D:
            self.dangerEdit.setCurrentIndex(2)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = NewFoldGen()
    w.show()
    sys.exit(app.exec_())


