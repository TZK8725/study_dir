import re
import os
import requests
from tqdm import tqdm
from gevent import monkey
import gevent
from fake_useragent import UserAgent
import pretty_errors
from Crypto.Cipher import AES
from retrying import retry


monkey.patch_all()
ua = UserAgent()

def get_ts(start_url):

    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 Edg/80.0.361.48"}
    response = requests.get(start_url, headers=headers)
    m3u8_url = re.findall("var playUrl = '(.*?)';", response.text)[0]
    # print(m3u8_url)
    m3u8_url_list1 = m3u8_url.split("/")
    response = requests.get(m3u8_url, headers=headers)
    # print(response.text)
    m3u8_url_list2 = response.text.split("\n")
    m3u8_index = "/".join(m3u8_url_list1[:-1])+"/"+m3u8_url_list2[-1]
    # print(m3u8_index)
    response = requests.get(m3u8_index, headers=headers)
    # print(response.text)
    video_url_header = "/".join(m3u8_index.split("/")[:-1])+"/"
    if "#EXT-X-KEY" in response.text:
        key_url = video_url_header + "key.key"
        response1 = requests.get(key_url, headers=headers)
        key = response1.content
    else:
        key = None
    ts_list = response.text.split("\n")    
    ts_list = [i for i in ts_list if i.endswith(".ts")]
    return ts_list, key, video_url_header
    # print(ts_list)
    # aes = AES.new(key, AES.MODE_CBC)

@retry(wait_random_min=0.5, wait_random_max=5)
def down_video(ts_list, key, base_url, num, name):
    if len(key) == 16:
        aes = AES.new(key, AES.MODE_CBC)
    for i in ts_list:
        try :
            if len(key) == 0:
                video = requests.get(base_url+i, headers={"User-Agent":ua.chrome})
                with open("F:/New folder/{}.ts".format(name+str(num)), "ab") as f:
                    f.write(video.content) 
            else:   
                video = requests.get(base_url+i, headers={"User-Agent":ua.chrome})
                with open("F:/New folder/{}.ts".format(name+str(num)), "ab") as f:
                    f.write(aes.decrypt(video.content))
                # print(i, "...")
        except:
            print(i, "*"*30)
    gevent.sleep()
        
                

# g1 = gevent.spawn(down_video, ts_list[ : int(len(ts_list)/4)], key)
# # g1.join()
# g2 = gevent.spawn(down_video, ts_list[int(len(ts_list)/4) : int(len(ts_list)/2)], key)
# # g2.join()
# g3 = gevent.spawn(down_video, ts_list[int(len(ts_list)/2) : int(len(ts_list)*3/4)], key)
# # g3.join()
# g4 = gevent.spawn(down_video, ts_list[int(len(ts_list)*3/4) : ], key)

def get_spawn(funtion, num:int, ts_list:list, key, base_url, *args, **kwargs):
    if len(args) != 0 and type(*args) is str:
        name = args
    else:
        name = "video_"
        
    g_list = list()
    for i in range(num):
        g = gevent.spawn(funtion, ts_list[ int(len(ts_list)*i/num): int(len(ts_list)*(i+1)/num)], key, base_url, i, name )
        g_list.append(g)
    gevent.joinall(g_list)
    # print(g_list)
def merge_ts(path:str):
    
    ts_list = os.listdir(path)
    ts_list = [os.path.join(path, i) for i in ts_list]
    # sorted(ts_list, lambda x : )
    # print(ts_list)
    with open("F:\\萌琪琪.ts", "ab") as f:
        for i in ts_list:
            with open(i, "rb") as f_:
                f.write(f_.read())


if __name__ == "__main__":

    ts_list, key, base_url = get_ts("http://www.92kpw.xyz/ff8080816c6b3d60016c6b4d043b3470.html")

    get_spawn(down_video, 10, ts_list, key, base_url)

    merge_ts("F:\\New folder")
    
    print("done")