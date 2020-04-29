import os
from random import sample
import shutil

new_path = r"E:\random_img"
img_list = os.listdir(r"E:\img_crawl2")
# print(img_list)
random_list = sample(img_list, 100)
random_list = [os.path.join("E:\img_crawl2", i) for i in random_list]
# print(random_list)
for path in random_list:
    shutil.copy2(path, new_path)