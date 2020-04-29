import requests
from selenium import webdriver
import time


class Msg(object):

    def __init__(self, phone_number):

        self.phone_number = phone_number
        self.windows_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        self.phone_headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'}

    def douban(self):
        self.douban_request_url = 'https://accounts.douban.com/j/mobile/login/request_phone_code'
        self.form_data = {'ck': '',
                          'area_code': '+86',
                          'number': '{}'.format(self.phone_number)}
        requests.post(self.douban_request_url, data=self.form_data,
                      headers=self.windows_headers)

    def it_home(self):
        browser = webdriver.Chrome()
        browser.get('https://my.ruanmei.com/?page=register')
        # browser.find_element_by_xpath('/html/body/div[12]/div[1]/div/div[2]/a').click()
        # browser.find_element_by_xpath('//*[@id="logins_window"]/div[1]/div[2]/div[2]').click()
        browser.find_element_by_xpath(
            '//*[@id="phone"]').send_keys(self.phone_number)
        browser.find_element_by_xpath('//*[@id="sendsms"]').click()
        
    def weibo(self):
        weibo_url = 'https://m.weibo.cn/api/login/sendsms'
        data = {'phone': self.phone_number,
                'st': 'false'}
        requests.post(weibo_url, data=data, headers=self.phone_headers)

    def neets(self):
        browser = webdriver.Chrome()
        browser.get('https://neets.cc/')
        browser.find_element_by_xpath(
            '/html/body/div[12]/div[1]/div/div[2]/a').click()
        browser.find_element_by_xpath(
            '//*[@id="logins_window"]/div[1]/div[2]/div[2]').click()
        browser.find_element_by_xpath(
            '//*[@id="tel"]').send_keys(self.phone_number)
        browser.find_element_by_xpath(
            '//*[@id="logins_window"]/div[2]/div[1]/div[2]/div[2]').click()

    def run(self):
        self.douban()
        time.sleep(10)
        self.weibo()
        time.sleep(10)
        self.it_home()
        time.sleep(10)
        self.neets()


if __name__ == '__main__':

    sabi = Msg('13159115487')
    sabi.run()
