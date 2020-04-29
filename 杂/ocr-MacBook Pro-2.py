from keyboard import wait
from PIL.ImageGrab import grabclipboard
from time import sleep
import baidu_ocr
import pyperclip

def get_input():
    x = input("请选择：\n保留自动换行-------------------1\n取消自动换行（适合截屏论文）---2\n输入1 或 2, 并按回车：")
    try:
        if int(x) == 2:
            print("取消自动换行\n")
            option = False
        elif int(x) == 1:
            option = True
            print("保留自动换行\n")
        else:
            print("SB !!!!\n默认取消自动换行\n")
            option = False
        return option
    except:
        print("SB !!!!你瞎按干什么？\n默认取消自动换行\n")
        return False


def screen_shot(option):
    i = 1
    while True:
        print ('-'*20,'{}'.format(i),'-'*20,end = '\n')
        if wait(hotkey='shift+win+s') == None:
            if wait(hotkey='ctrl') == None:
                sleep(0.01)
                try:
                    img = grabclipboard()
                    img.save('picture.png')
                except:
                    print('请重新截图')
                    screen_shot()
                i+=1                
                alltexts = baidu_ocr.get_text(option)
                sleep(0.2)
                # w.OpenClipboard()

                # d=w.GetClipboardData(win32con.CF_UNICODETEXT)
                # w.CloseClipboard()'''
                # OpenClipboard()
                # EmptyClipboard()
                # SetClipboardData(win32con.CF_UNICODETEXT, alltexts)
                # CloseClipboard()
                pyperclip.copy(alltexts)


if __name__ == "__main__":
    op = get_input()
    print('Tip:\n 1.按住Shift + win + s 进行截图(win10)\n 2.按一下 ctrl 进行文字识别 \n 3.右键粘贴(不需要复制窗口文字,可将窗口最小化运行)')
    print('-'*50,'by Kun\n')
    screen_shot(op)
    # ctrl_c()
