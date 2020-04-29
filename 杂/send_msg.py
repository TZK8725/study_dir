import requests
import yagmail
import os

class SendMsg(object):

    def __init__(self):

        self.header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}

        self.sever_chan_url = 'https://sc.ftqq.com/SCU53140Tb9f5e03ced7cc1fdef72f77aa6289d875cfd28e3cbd9a.send'

        self.sm_url = 'https://sm.ms/api/upload'

    def to_email(self, subject, content):
        '''
            subject : 邮件主题\n
            content ：发送内容
        '''

        yag=yagmail.SMTP(user='tzk872579163@live.com', password='LZS...1230', port=587,host='smtp.office365.com', smtp_ssl=False)
        yag.send(to='tzk872579163@live.com', subject=subject, contents=content)

    def server_chan(self,title,content):

        '''推送简单消息到微信\n 
            title,content
        '''

        data = {
                'text': title,'desp': content
                }
        response = requests.post(self.sever_chan_url, data)
        print(response.text)

    def _sm(self,path):
        if os.path.isfile(path):
            with open (path, 'rb') as f :
                img = f.read()
        else :
            return(path)

        file = {'smfile':img}
        response = requests.post(self.sm_url, files=file, headers=self.header)
        response=response.json()
        if response['code'] == 'success' :
            return (response['data']['url'])
        else:
            print('上传失败')
            return (path)
            
    def server_img(self, title, path):

        '''向微信推送图片\n
            path'''

        img_url = self._sm(path)
        img = '![img]({})'.format(img_url)
        self.server_chan(title,img)
