import os
import datetime
import cv2
from keras.models import load_model
import numpy as np


startime = datetime.datetime.now()


def shut_down():

    os.system('shutdown -s -f -t 0')


def face_rec():
    m = load_model(r'C:\Users\TZK\Desktop\学习\dataset\deep learning\model\face.h5')
    cap = cv2.VideoCapture(0)
    classifier = cv2.CascadeClassifier(r'G:\onedrive\py\study_dir\haarcascade_xml\haarcascade_frontalface_alt2.xml')
    color = (0, 255, 196)
    ret = True
    i = 0
    results = list()
    rates = [[1]]
    while ret:
        endtime = datetime.datetime.now()
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        facerects = classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(32, 32))
        if len(facerects) > 0 and i < 10:

            x, y, w, h = facerects[0]
            cv2.rectangle(frame, (x-10, y-10), (x+w+10, y+h+10), color=color, thickness=2)
            image = frame[  ]
            image = cv2.resize(image, (64, 64))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            image = np.array(image)
            image = np.reshape(image, newshape=(1, 64, 64, 1))
            result = m.predict_classes(image)
            rates = m.predict(image)
            # rates.append(rate[0][0])
            results.append(result[0])
            # cv2.imwrite(r'C:\Users\TZK\Desktop\学习\dataset\face\{}.jpg'.format(i), img=image)
            i += 1
            print(rates[0])
        cv2.imshow('TZK', frame)
        if sum(results) != 0 or rates[0][0] < 0.99:
            # MessageBox(win32con.NULL, u'操你妈！！！', u'认证失败', win32con.MB_OK)
            # shut_down()
            pass

        if i >= 10:
            break
        if int((endtime - startime).seconds) > 50:
            # MessageBox(win32con.NULL, u'操你妈！！！', u'认证失败', win32con.MB_OK)
            shut_down()
        c=cv2.waitKey(10)


if __name__ == '__main__':
    face_rec()
