from PIL import Image
import os
import random
import time
import tqdm


def get_image_ctime(img_list):

    newImageList = list()
    imgDict = dict()
    for i in img_list:
        
        imgCtime = os.path.getctime(i)
        imgDict[str(imgCtime)] = i
        newImageList.append(imgCtime)
    # print([imgDict[str(i)] for i in newImageList])
    newImageList.sort()
    # print(newImageList)
    # print([imgDict[str(i)] for i in newImageList])
    return [imgDict[str(i)] for i in newImageList]




x = input(r"路径:")
imagePath = x
imageList = os.listdir(imagePath)
#4032, 3024
# print(imageList)
for imgDir in tqdm.tqdm(imageList):
    imgAllDir = os.path.join(imagePath, imgDir)
    # print(imgAllDir)
    img_list = [os.path.join(imgAllDir, i) for i in os.listdir(imgAllDir)]
    img_list = get_image_ctime(img_list)
    # print(img_list)
    # if "heic" not in img_list[1]:
    try:
        if len(img_list) < 6:
            if len(img_list) == 3 or 5:
                image = Image.open(img_list[1])
                for i in range(6-len(img_list)):
                    # print(image.size)
                    x = random.randint(0, 2000)
                    y = random.randint(0, 1400)
                    box = (x, y, x+2000, y+1600)
                    img = image.crop(box)
                    img.save(imgAllDir+"\{}.JPG".format(time.time()))
            elif len(img_list) == 4:
                image1 = Image.open(os.path.join(imgAllDir, img_list[1]))
                image2 = Image.open(os.path.join(imgAllDir, img_list[2]))

                x1 = random.randint(0, 2000)
                y1= random.randint(0, 1000)
                x2 = random.randint(0, 2000)
                y2 = random.randint(0, 1000)
                box1 = (x1, y1, x1 + 2000, y1 + 1600)
                box2 = (x2, y2, x2 + 2000, y2 + 1600)
                img1 = image1.crop(box1)
                img2 = image2.crop(box2)
                img1.save(imgAllDir+"\{}.JPG".format(time.time()))
                img2.save(imgAllDir+"\{}.JPG".format(time.time()))
    except :
        pass