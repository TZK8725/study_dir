import sys
import cv2
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from PyQt5.QtGui import QFont, QPixmap, QImage
import img_pre
import numpy as np


class DetectWindows(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.break_sign = 0

    def initUI(self):

        self.setWindowTitle("智能控制系统仿真")
        self.resize(1200, 700)
        faceButton = QPushButton("人脸识别", self )
        bodyButton = QPushButton("行人检测", self)
        signButton = QPushButton("交通标志识别", self)
        startButton = QPushButton("开始", self)
        faceButton.move(100, 600)
        bodyButton.move(250, 600)
        signButton.move(400, 600)
        startButton.move(550, 600)
        cameraLabel = QLabel("Video:", self)
        detectLabel = QLabel("Detect:", self)
        kunLabel = QLabel("By Kun", self)
        self.imageLabel = QLabel(self)
        self.detectImageLabel = QLabel(self)
        self.detectImageLabel.move(850, 50)
        self.imageLabel.resize(640, 480)
        self.imageLabel.move(50, 50)
        self.resultLabel = QLabel(self)
        self.resultLabel.move(800, 500)
        self.resultLabel.resize(200, 40)
        kunLabel.move(800, 650)
        cameraLabel.move(20, 20)
        detectLabel.move(800, 20)

        startButton.clicked.connect(self.videoShow)
        faceButton.clicked.connect(self.faceDetect)
        bodyButton.clicked.connect(self.bodyDetect)
        signButton.clicked.connect(self.singDetect)

    def videoShow(self):

        ret = 1
        cap = cv2.VideoCapture(0)
        while ret:
            ret, frame = cap.read()
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            _image = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
            self.imageLabel.setPixmap(QPixmap(_image))
            cv2.waitKey(20)
            if self.break_sign:
                break

    def faceDetect(self):
        # print(self.sender().text())
        ret = 1
        cap = cv2.VideoCapture(0)
        haar_file = r"H:\Anaconda\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml"
        classifier = cv2.CascadeClassifier(haar_file)
        while ret:
            ret, frame = cap.read()
            # print(frame.shape)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            _image = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
            self.imageLabel.setPixmap(QPixmap(_image))
            faces = classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48))
            if len(faces):
                x, y, w, h = faces[0]
                face_img = frame[y-20: y+h+20, x-20: x+w+20]
                # print(face_img.shape)
                face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                face_image = QImage(face_img_rgb, face_img.shape[1], face_img.shape[0], face_img.shape[1] * 3,
                                    QImage.Format_RGB888)
                # self.detectImageLabel.resize(face_img.shape[0], face_img.shape[1])
                self.detectImageLabel.resize(128, 128)
                self.detectImageLabel.setPixmap(QPixmap(face_image).scaled(128, 128))
            cv2.waitKey(10)
            if self.break_sign:
                break

    def bodyDetect(self):

        ret = 1
        hog = cv2.HOGDescriptor()
        cap = cv2.VideoCapture(0)
        while ret:
            ret, frame = cap.read()
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            _image = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
            self.imageLabel.setPixmap(QPixmap(_image))
            h, w, c = frame.shape
            image = cv2.resize(frame, (int(w / 2), int(h / 2)))
            detect_image = image
            hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
            locations, weights = hog.detectMultiScale(detect_image, scale=1.09, winStride=(8, 8))
            # print(locations, weights)
            for body, w in zip(locations, weights):
                if w > 0.5:
                    x, y, w, h = body
                    body_image = frame[y*2: (y+h)*2, x*2: (x+w)*2]
                    body_img_rgb = cv2.cvtColor(body_image, cv2.COLOR_BGR2RGB)
                    body_image_ = QImage(body_img_rgb, body_img_rgb.shape[1], body_img_rgb.shape[0],
                                         body_img_rgb.shape[1] * 3, QImage.Format_RGB888)
                    self.detectImageLabel.resize(body_image.shape[1], body_image.shape[0])
                    self.detectImageLabel.setPixmap(QPixmap(body_image_))
            cv2.waitKey(10)

            if self.break_sign:
                break

    def singDetect(self):

            cap = cv2.VideoCapture(0)
            ret = 1
            while ret:

                ret, frame = cap.read()
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                _image = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
                self.imageLabel.setPixmap(QPixmap(_image))
                img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask1 = cv2.inRange(img_hsv, np.array([0, 46, 46]), np.array([10, 255, 255]))
                mask2 = cv2.inRange(img_hsv, np.array([156, 46, 46]), np.array([180, 255, 255]))
                mask = mask1 + mask2
                mask_blur = cv2.medianBlur(mask, ksize=9)

                # kernel_1 = np.ones((3, 3), np.uint8)
                # kernel_2 = np.ones((7, 7), np.uint8)
                # erode = cv2.erode(mask_blur, kernel_1)
                # dilate = cv2.dilate(erode, kernel_2)

                w, h = np.shape(frame)[:2]
                # cv2.floodFill(dilate, np.zeros((w+2, h+2), np.uint8), (0, 0), (0, 0, 0))
                # contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                img_new = np.zeros([w, h], np.uint8)
                # for contour in contours:
                #     cv2.drawContours(img_new, [contour], -1, (255, 255, 255), -1)
                # img_edge2 = cv2.Canny(mask, 50, 150)
                img_edge = cv2.Canny(mask_blur, 50, 100)
                hough = cv2.HoughCircles(img_edge, cv2.HOUGH_GRADIENT, minDist=50, dp=1, param2=30, minRadius=33,
                                         maxRadius=100)
                text_x, text_y = 0, 0
                new_img = None
                try:
                    for i in hough[0]:
                        # print(i)
                        x = int(i[0]) - int(i[2]) - 8
                        y = int(i[1]) - int(i[2]) - 8
                        w = 2 * int(i[2]) + 8
                        h = 2 * int(i[2]) + 8
                        new_img = frame[y:y + h, x:x + w]
                        text_x, text_y = x, y
                except:
                    pass

                if new_img is not None:
                    y, x = new_img.shape[:2]
                    if (x and y) > 64:
                        result = img_pre.recognition(new_img)
                        self.resultLabel.setText("Result:%s"%result[0])
                        sign_img_rgb = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
                        sign_image = QImage(sign_img_rgb, sign_img_rgb.shape[1], sign_img_rgb.shape[0],
                                            sign_img_rgb.shape[1] * 3, QImage.Format_RGB888)
                        # self.detectImageLabel.resize(face_img.shape[0], face_img.shape[1])
                        self.detectImageLabel.resize(128, 128)
                        self.detectImageLabel.setPixmap(QPixmap(sign_image).scaled(128, 128))
                cv2.waitKey(10)
                if self.break_sign:
                    break

    def closeEvent(self, e):
        self.break_sign = 1

    def cv2QtImage(self, cv_image):

        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        qt_image = QImage(rgb_image, rgb_image.shape[1], rgb_image.shape[0], rgb_image.shape[1] * 3,
                          QImage.Format_RGB888)
        return qt_image


if __name__ == "__main__":

    app = QApplication(sys.argv)
    dw = DetectWindows()
    dw.show()
    sys.exit(app.exec_())