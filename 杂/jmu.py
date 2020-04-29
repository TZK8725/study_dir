import urllib
import requests
from lxml import etree
import pandas as pd
import database

# cookies = {"Cookie" : "_sp_id.acfd=7b720cae-a83d-482e-920a-01c9a12ef3b7.1581944349.1.1581944349.1581944349.15c80c74-b932-449f-a66c-4ff871579ddf; ASP.NET_SessionId=nn0rtc3bug0ias55s13hzt55"}
# headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36 Edg/80.0.361.53"}
# url = "http://jwgls.jmu.edu.cn/Student/ScoreCourse/ScoreAll.aspx"
# # form = {"__EVENTTARGET": "ctl00$ContentPlaceHolder1$gotoNextPage", "ctl00$ContentPlaceHolder1$pageNumber": 100, "__VIEWSTATE" : "/wEPDwULLTEzNDkxMjMzODEPZBYCZg9kFgICBQ9kFgICAw9kFgQCAQ8QZBAVCA/mjInlrablubTlrabmnJ8bMjAxNi0yMDE35a2m5bm056ys5LiA5a2m5pyfGzIwMTYtMjAxN+WtpuW5tOesrOS6jOWtpuacnxsyMDE3LTIwMTjlrablubTnrKzkuIDlrabmnJ8bMjAxNy0yMDE45a2m5bm056ys5LqM5a2m5pyfGzIwMTgtMjAxOeWtpuW5tOesrOS4gOWtpuacnxsyMDE4LTIwMTnlrablubTnrKzkuozlrabmnJ8bMjAxOS0yMDIw5a2m5bm056ys5LiA5a2m5pyfFQgABTIwMTYxBTIwMTYyBTIwMTcxBTIwMTcyBTIwMTgxBTIwMTgyBTIwMTkxFCsDCGdnZ2dnZ2dnFgFmZAIFD2QWAmYPZBYCZg9kFgwCAQ8WAh4EVGV4dAUBMWQCBA8QZGQWAWZkAgYPFgIfAAUCNzdkAggPFgIfAAUBNGQCCw8PFgIeB0VuYWJsZWRoZGQCDQ8PFgIfAWhkZGS7mUTLXzhCJoy+pes2V0ORKCxglg=="}
# form = {"__EVENTTARGET": "ctl00$ContentPlaceHolder1$gotoNextPage", "ctl00$ContentPlaceHolder1$pageNumber": 100}
# response = requests.post(url, headers=headers, cookies=cookies, data=form)
# print(response.text)

# with open(r"G:\\score.html", "w", encoding="utf-8") as f:
#     f.write(response.text)

with open (r"G:\\score.html", "r", encoding="utf-8") as f:
    html = f.read()

html : etree._Element = etree.HTML(html)

tr_list = html.xpath("body/table//tr[2]//div//table[@id='ctl00_ContentPlaceHolder1_scoreList']//tr")
# print(len(tr_list))

all_items = []
names = tr_list[0].xpath(".//td/text()")
print(names)
for tr in tr_list[1 : ] :
    items = {}
    item = tr.xpath(".//td/text()")
    num = 0
    for i, num in zip(item, range(len(item))):
        # print(i)
        items[names[num]] = i
        

    all_items.append(items)
# print(all_items[0]["学分"])
s = list()
for i in all_items:
    # print(i["学分"])
    s.append(float(i["学分"]))
    

# print("总学分为：", sum(s))
# database.post("Jmu", "score", all_items)
