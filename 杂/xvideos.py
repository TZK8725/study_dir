import requests
import re
import time
import datetime


class Xvideos_Downloader(object):

    def __init__(self, star_url, name='xv'):
        self.name = name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
        self.star_url = star_url
        self.headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}

    def find_base_url(self):
        response = requests.get(self.star_url, headers=self.headers)
        star_m3u8_url = re.findall(
            r"setVideoHLS\('(.*?)'\)", response.content.decode())  # 查找储存清晰度的m3u8地址
        self.star_m3u8_url = star_m3u8_url[0]
        m3u8 = requests.get(self.star_m3u8_url, headers=self.headers)
        m3u8_last_url = ''
        if '720' in m3u8.text:
            m3u8_last_url += 'hls-720p.m3u8'
            print('下载码率为 720p')
        elif '480' in m3u8.text:
            m3u8_last_url += 'hls-480p.m3u8'
            print('下载码率为 480p')
        elif '360' in m3u8.text:
            m3u8_last_url += 'hls-360p.m3u8'
            print('下载码率为 360p')
        elif '250' in m3u8.text:
            m3u8_last_url += 'hls-250p.m3u8'
            print('下载码率为 250p')
        else:
            print('not find')

        # 选择最清晰的下载
        self.m3u8_last_url = self.star_m3u8_url.replace(
            'hls.m3u8', m3u8_last_url)

    def find_ts_url(self):  # 查找下载ts文件的m3u8
        response = requests.get(self.m3u8_last_url, headers=self.headers)
        self.ts_url_lists = response.text.split('\n')
        self.ts_lists = []
        for ts_url in self.ts_url_lists:
            if ts_url.startswith('hls'):
                self.ts_lists.append(ts_url)
        print('视频时长: %.2f min' % (len(self.ts_lists)/6))

    def save(self):
        startime = datetime.datetime.now().replace(microsecond=0)
        i = 1
        for ts_url in self.ts_lists:
            ts_last_url = self.star_m3u8_url.replace('hls.m3u8', ts_url)
            print('saving:%.2f ' % ((i/len(self.ts_lists))*100), r'%', end='\r')
            try:
                time.sleep(1)
                ts = requests.get(
                    ts_last_url, headers=self.headers)
            except:
                time.sleep(5)
                ts = requests.get(ts_last_url, headers=self.headers2)
            finally:
                if ts.content is not None:
                    with open(r'C:\Users\TZK\Desktop\{}.ts'.format(self.name), 'ab') as f:
                        f.write(ts.content)
                else:
                    print('网络出错')
        endtime = datetime.datetime.now()
        # print(endtime)
        print('Download over!!!用时 %s 秒\n撸她!!! ' % (endtime-startime).seconds)

    def run(self):
        startime = datetime.datetime.now()
        print(startime)
        self.find_base_url()
        self.find_ts_url()
        self.save()


if __name__ == "__main__":
    xd = Xvideos_Downloader(
        'https://www.xvideos.com/video28457799/korean_porn_shin_min_ah_-_hdporn.vip', '22')
    xd.run()
