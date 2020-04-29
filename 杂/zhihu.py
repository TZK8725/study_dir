import re
import os
from urllib.parse import urlencode
import requests
import json

id_num = 274637437
base_url = "https://www.zhihu.com/api/v4/questions/%d/answers?"%id_num
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3891.0 Safari/537.36 Edg/78.0.268.3",
'cookie': '_zap=33eba819-cefc-473f-97f9-44b06d6a8eac; d_c0="AKDiaKsewg-PTrQVh9XQCC3ad1_-81lpe7Y=|1563505197"; _xsrf=TpILnUyRRA6pa6z1ChvpC0aCRpmlbxIY; capsion_ticket="2|1:0|10:1568534347|14:capsion_ticket|44:MjU5ZmVlNmUyOTMxNGNmNjk5Y2U3N2ExNTZmY2UzNzE=|a7944c5601293d3100a135c1d35f80d9b6b60c1c42261c280acd20804d9e7384"; z_c0="2|1:0|10:1568534383|4:z_c0|92:Mi4xaE1tV0F3QUFBQUFBb09Kb3F4N0NEeWNBQUFDRUFsVk5iM3lsWFFBS0JoOXZnT3l4YUtXN082STZNMDktbFRrWlZR|96e171f822ec1dea8b46c92b3d25ae4b3f2dc01ca88624d0421f6af89fb1db59"; tst=r; q_c1=b5fd22f554ba4c24acfdef92b1ff3a50|1568535973000|1568535973000; tgw_l7_route=7f546500f1123d2f6701ac7f30637fd6',
'referer': 'https://www.zhihu.com/question/313825759/answer/732128046',
'x-requested-with': 'fetch'}
parameters = {
    "include": "data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics",
    "offset": "",
    "limit": 3,
    "sort_by": "default",
    "platform": "desktop"
    }
start_url = base_url + urlencode(parameters)

def parse(url):
    i = 0
    response = requests.get(url, headers=headers)
    # print(response.content.decode())
    content = json.loads(response.text)
    __id = content["data"][0]["id"]
    img_list = re.findall(r"https://pic2.zhimg.com/50/.*?_hd.jpg", content["data"][0]["content"])
    if len(img_list)>0:
        for img_url in list(set(img_list)):
            img = requests.get(img_url, headers=headers)
            with open (r'C:\Users\TZK\Desktop\学习\zhihu\{}.{}.jpg'.format(_id, i), "wb") as f:
                f.write(img.content)
            if os.path.getsize(r'C:\Users\TZK\Desktop\学习\zhihu\{}.{}.jpg'.format(_id, i)) <15000:
                os.remove(r'C:\Users\TZK\Desktop\学习\zhihu\{}.{}.jpg'.format(__id, i))
            else:
                i+=1

    next_url = content["paging"]["next"]
    # print(content["paging"]["is_end"])
    if not content["paging"]["is_end"] :
        parse(next_url)


if __name__ == "__main__":
    parse(start_url)