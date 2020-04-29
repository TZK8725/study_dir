import os
import pyheif
from PIL import Image

def heic2jpg():

    path = "/Users/kun/Desktop/岐下村"
    total_dir = [os.path.join(path, i) for i in os.listdir(path)]
    # print(total_dir)

    for img_dir in total_dir:
        if "DS_S" in img_dir:
            pass
        else:
            img_list = [os.path.join(img_dir, i)for i in os.listdir(img_dir)]
            for img in img_list:
                if "heic" in img:
                    print(2)
                    img_name = img.split("/")[-1]
                    hi_img = pyheif.read_heif(img)
                    jpg_img = Image.frombytes(data=hi_img.data, size=hi_img.size, mode=hi_img.mode)
                    jpg_img.save(img_dir+"/%s.jpg"%img_name)
                    os.remove(img)


heic2jpg()
