import os

x = input(r"地址：")
img_dir_list = [os.path.join(x, i) for i in os.listdir(x)]
for dir_path in img_dir_list:
    img_list = [os.path.join(dir_path, j) for j in os.listdir(dir_path)]
    i = 1
    for img in img_list:
        image_type = img.split(".")[-1]
        os.rename(img, dir_path+"/%d."%i+image_type)
        i += 1