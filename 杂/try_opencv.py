import cv2
import datetime
from  os import remove,getcwd ,path
import send_msg


def play_video(path):
    cap = cv2.VideoCapture(path)
    #cap_get=cv2.VideoCapture
    fps=cap.get(cv2.CAP_PROP_FPS)
    ret,frame=cap.read()  
    #print(fps)
    while ret : 

        cv2.imshow(r'frame',frame)
        cv2.waitKey(int(fps))
        ret,frame=cap.read()
    cap.release()
    cv2.destroyAllWindows()


def send_cap():
    t = datetime.datetime.now()       
    cap = cv2.VideoCapture(0)
    f,frame=cap.read()

    cv2.imwrite('example.png',frame)
    cap.release()
    sendmsg = send_msg.SendMsg()
    sendmsg.server_img('{}'.format(t),r'{}/example.png'.format(getcwd()))
    #yag_email.send_email('{}'.format(datetime.now()),r'{}\example.png'.format(getcwd()))
    #remove(r'{}/example.png'.format(getcwd()))

if __name__ == "__main__":
    send_cap()