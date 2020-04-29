from lxml import etree
import requests
from PIL import ImageShow, Image
import pandas as pd


print("截止到2020/02/20 软件测试无误，由于学校登录系统有个登录状态码是加密的，所以可能随时失败，软件不兼容的联系班里最帅的那个帮忙导吧。。\n我已人品担保不会上传你的账号密码\n", "_"*30)
username = int(input("学号："))
password = str(input("密码："))
image_url = "http://jwgls.jmu.edu.cn/Common/CheckCode.aspx"
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36 Edg/80.0.361.53"}
s = requests.Session()
response = s.get(image_url, headers=headers)
with open(r"check.jpg", "wb") as f:
    f.write(response.content)
try:
    check_image = Image.open(r"check.jpg")
    ImageShow.show(check_image, title="验证码")
except:
    print("抱歉显示验证码失败，请直接退出")
code = input("验证码：")
# plt.show()
data = {
    "__VIEWSTATE":"/wEPDwUKMTA4MDEzMTMyOQ9kFgICAw9kFgICDw8PFgIeBFRleHQFATBkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUNQnRuTG9naW5JbWFnZQUNQnRuUmVzZXRJbWFnZcH71Q3NhGesjfuvAIN4VJIH4TsM",
    "TxtUserName": username,
    "TxtPassword": password,
    "TxtVerifCode": int(code),
    "BtnLoginImage.x":33,
    "BtnLoginImage.y":7
    }
login_url = "http://jwgls.jmu.edu.cn/login.aspx"
# print(data)
response = s.post(login_url, headers=headers, data=data)
score_url = "http://jwgls.jmu.edu.cn/Student/ScoreCourse/ScoreAll.aspx"
form = {"__EVENTTARGET": "ctl00$ContentPlaceHolder1$gotoNextPage", "ctl00$ContentPlaceHolder1$pageNumber": 200}
response = s.post(score_url,data=form, headers=headers)
# print(response.text)
if "我的课程成绩" in response.text:
    print(True)
    html : etree._Element = etree.HTML(response.text)
    tr_list = html.xpath("body/table//tr[2]//div//table[@id='ctl00_ContentPlaceHolder1_scoreList']//tr")

    all_items = []
    names = tr_list[0].xpath(".//td/text()")
    # print(names)
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

        if ("不合格" and "不及格") not in i["成绩"]:
            try:
                if float(i["成绩"]) >= 60:
                    s.append(float(i["学分"]))

            except:
                s.append(float(i["学分"]))

    print("总合格学分为：", sum(s))
    items = pd.DataFrame(all_items)
    # print(items)
    # items.to_excel(r"C:\Users\TZK\Desktop\score.xlsx", encoding='ANSI',index=False, sheet_name="sheet1", na_rep="")
    items.to_csv(r"score.csv", encoding='ANSI', index=False)
    data = pd.read_csv(r"score.csv", encoding='ANSI')
    data.to_excel(r"{}.xlsx".format(username), encoding='utf-8',index=False, sheet_name="sheet1", na_rep="")
    print("导出成功！！")
    input("按enter键退出")
else:
    print("登录错误，请重试ヾ(≧▽≦*)o")
    input("按enter键退出")

