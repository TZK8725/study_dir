import time
from appium import webdriver
import pyppeteer
import asyncio
from lxml import etree
from matplotlib import pyplot as plt


# from pyquery import PyQuery as pq

async def main():

    
    browser = await pyppeteer.launch(headless=False, userDataDir="C:\\Users\\TZK\\Desktop\\学习\\userData")
    page = await browser.newPage()
    await page.goto('https://www.xuexi.cn/')
    time.sleep(2)
    pages = await browser.pages()
    if len(pages) != 1:
        page_new = pages[0]
        await page_new.close()
    await page.click("#root > div > header > div.menu > div.login > a.icon.login-icon")
    time.sleep(3)
    # print(type(page))
    # doc = pq(await page.content())
    tap_list = await page.xpath("//span[@class='text']")
    # print(tap_list[:1])
    # x_list = await page.Jx("//span[@class='text']")
    # print(x_list)
    for tap_ in tap_list[:1]:
        # print(tap_)
        await tap_.click()
        await asyncio.sleep(5)
    page_list = await browser.pages()
    # print(page_list, page)
    page_2 = page_list[-1]
    await page_2.close()
    time.sleep(3)
    await browser.close()
 
# asyncio.get_event_loop().run_until_complete(main())

def win_swipe(window_size:dict):

    driver.swipe(x/2, y/2, x/2, y/2-300, 1000)

desired_caps = dict()
desired_caps["platformName"] = "Android"
desired_caps["platformVersion"] = "7.1.2"
desired_caps["appPackage"] = "cn.xuexi.android"
desired_caps["appActivity"] = "com.alibaba.android.rimet.biz.SplashActivity"
desired_caps["deviceName"] = "e6c9f2557d84 device" #"e6c9f2557d84 device"
desired_caps["noReset"] = "true"
desired_caps["autoGrantPermissions"] = "true"
desired_caps["skipDeviceInitialization"] = "true"
desired_caps["skipServerInstallation"] = "true"
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
print(driver.current_activity)
time.sleep(10)
window_size = driver.get_window_size()
x = window_size["width"]
y = window_size["height"]

driver.tap([(x/2, y/2+200)], 500)
time.sleep(5)
for i in range(5):
    driver.swipe(x/2, y/2, x/2, y/2-300)
    time.sleep(5)

driver.back()
# driver.swipe(100, 100, 150, 150)
time.sleep(5)
driver.quit()
