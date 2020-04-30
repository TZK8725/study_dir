import sys
import os
import cv2
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QStatusBar, QMainWindow
from PyQt5.QtGui import QFont, QPixmap, QImage
import joblib
import numpy as np
from skimage.feature import hog
import baiduface


class DetectWindows(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.break_sign = 0
        self.detect_class = 0

        haar_file = r"H:\Anaconda\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml"
        self.classifier = cv2.CascadeClassifier(haar_file)
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.sign_classifier = joblib.load("./model.pkl")

    def initUI(self):

        """初始化窗口组件"""
        self.setWindowTitle("智能控制系统仿真")
        self.resize(1200, 700)
        self.setMaximumSize(1200, 700)
        self.setMinimumSize(1200, 700)
        self.faceButton = QPushButton("人脸识别", self)
        self.bodyButton = QPushButton("行人检测", self)
        self.signButton = QPushButton("交通标志识别", self)
        startButton = QPushButton("开始", self)

        self.faceButton.move(100, 600)
        self.bodyButton.move(250, 600)
        self.signButton.move(400, 600)
        startButton.move(550, 600)

        cameraLabel = QLabel("<font size=5 face='Monaco'>Video:</font>", self)
        detectLabel = QLabel("<font size=5 face='Monaco'>Detect:</font>", self)
        kunLabel = QLabel("<font size=5 face='Monaco'>By Kun</font>", self)
        self.imageLabel = QLabel(self)
        self.detectImageLabel = QLabel(self)
        self.detectImageLabel.move(850, 50)
        self.imageLabel.resize(640, 480)
        self.imageLabel.move(50, 50)
        self.resultLabel = QLabel(self)
        self.resultLabel.move(800, 500)
        self.resultLabel.resize(400, 60)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.detectButton = QPushButton("识别", self)
        self.detectButton.move(1000, 350)
        self.detectButton.hide()
        self.detectButton.clicked.connect(self.faceMatch)

        kunLabel.move(1000, 650)
        cameraLabel.move(20, 20)
        detectLabel.move(800, 20)

        startButton.clicked.connect(self.videoShow)
        self.faceButton.clicked.connect(self.changeDetectClass)
        self.faceButton.setEnabled(False)
        self.bodyButton.clicked.connect(self.changeDetectClass)
        self.bodyButton.setEnabled(False)
        self.signButton.clicked.connect(self.changeDetectClass)
        self.signButton.setEnabled(False)

        self.setObjectName("MainWindow")
        # self.resultLabel.setObjectName("resultLabel")
        self.setStyleSheet("#MainWindow{border-image:url(C:/Users/TZK/Desktop/学习/T.jpg);}")
        # self.setWindowOpacity(0.95)

    def videoShow(self):

        """摄像头读取"""
        ret = 1
        cap = cv2.VideoCapture(0)
        self.signButton.setEnabled(True)
        self.faceButton.setEnabled(True)
        self.bodyButton.setEnabled(True)
        self.setStyleSheet("")
        while ret:
            ret, frame = cap.read()
            image = self.cv2QtImage(frame)
            self.imageLabel.setPixmap(QPixmap(image))

            if self.detect_class == 1:
                self.faceDetect(frame)
                self.current_image = frame
            elif self.detect_class == 2:
                self.bodyDetect(frame)
            elif self.detect_class == 3:
                self.signDetect(frame)

            cv2.waitKey(20)
            if self.break_sign:
                break

    def changeDetectClass(self):

        # 改变识别模式
        self.detectImageLabel.clear()
        self.resultLabel.clear()
        self.detectButton.hide()
        if self.sender().text() == "人脸识别":
            self.detect_class = 1
        elif self.sender().text() == "行人检测":
            self.detect_class = 2
        elif self.sender().text() == "交通标志识别":
            self.detect_class = 3
        # print(self.detect_class)
        self.status_bar.showMessage("当前模式: %s" % self.sender().text())

    def faceDetect(self, image):

        """人脸检测"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist_image = cv2.equalizeHist(gray)
        faces = self.classifier.detectMultiScale(hist_image, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48))
        if len(faces):
            x, y, w, h = faces[0]
            face_ROI = image[y - 40: y + h + 40, x - 40: x + w + 40]
            face_image = self.cv2QtImage(face_ROI)
            self.detectImageLabel.resize(256, 256)
            self.detectImageLabel.setPixmap(QPixmap(face_image).scaled(256, 256))
            if self.detectButton.isHidden():
                self.detectButton.show()

    def bodyDetect(self, image):

        """行人检测"""
        h, w, c = image.shape
        detect_image = cv2.resize(image, (int(w / 2), int(h / 2)))
        locations, weights = self.hog.detectMultiScale(detect_image, scale=1.09, winStride=(8, 8))
        for body, w in zip(locations, weights):
            body_count = len([i for i in weights if i > 1])
            if w > 0.9:
                x, y, w, h = body
                body_image = image[y * 2: (y + h) * 2, x * 2: (x + w) * 2]
                body = self.cv2QtImage(body_image)
                self.detectImageLabel.resize(body_image.shape[1], body_image.shape[0])
                self.detectImageLabel.setPixmap(QPixmap(body))
                self.resultLabel.setText("<font size=5 face='Monaco'>检测到%d处有行人</font>" % body_count)

    def signDetect(self, image):

        """交通标志检测"""
        img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(img_hsv, np.array([0, 46, 46]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(img_hsv, np.array([156, 46, 46]), np.array([180, 255, 255]))
        mask = mask1 + mask2
        mask_blur = cv2.medianBlur(mask, ksize=9)

        w, h = np.shape(image)[:2]
        img_new = np.zeros([w, h], np.uint8)
        img_edge = cv2.Canny(mask_blur, 50, 100)
        hough = cv2.HoughCircles(img_edge, cv2.HOUGH_GRADIENT, minDist=50, dp=1, param2=30, minRadius=33,
                                 maxRadius=100)
        sign = None
        try:
            for i in hough[0]:
                # print(i)
                x = int(i[0]) - int(i[2]) - 8
                y = int(i[1]) - int(i[2]) - 8
                w = 2 * int(i[2]) + 8
                h = 2 * int(i[2]) + 8
                sign = image[y:y + h, x:x + w]
        except Exception as e:
            pass

        if sign is not None:
            y, x = sign.shape[:2]
            if (x and y) > 64:
                result = self.sign_recongnition(sign)
                self.resultLabel.setText("<font size=4 face='Monaco'>Result: </font> <font size=6 color='#f08080' face='Monaco'>%s </font> " % result[0])
                self.detectImageLabel.resize(256, 256)
                sign_image = self.cv2QtImage(sign)
                self.detectImageLabel.setPixmap(QPixmap(sign_image).scaled(256, 256))

    def sign_recongnition(self, sign_image):

        """交通标志识别"""
        img = cv2.resize(sign_image, (64, 64))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        feature = hog(gray)
        features = [feature]
        result = self.sign_classifier.predict(features)
        return result

    def faceMatch(self):

        """人脸匹配"""
        cv2.imwrite("./unknown.jpg", self.current_image)
        face = baiduface.BaiduFace()
        verify_score, face_token, access_token = face.face_verify("./unknown.jpg")
        match_score, match_name = face.face_compare(face_token, access_token)
        os.remove("./unknown.jpg")
        self.resultLabel.setText("姓名: %s\n活体检测得分: %d\n人脸匹配得分: %d" % (match_name, verify_score*100, match_score))

    def closeEvent(self, e):
        self.break_sign = 1

    @staticmethod
    def cv2QtImage(cv_image):

        """将opencv image 转为 Qt image"""
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        qt_image = QImage(rgb_image, rgb_image.shape[1], rgb_image.shape[0], rgb_image.shape[1] * 3,
                          QImage.Format_RGB888)
        return qt_image


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    dw = DetectWindows()

    dw.show()
    sys.exit(app.exec_())