import cv2
import time
import numpy as np
from skimage.feature import hog as skhog


body_image = cv2.imread(r"C:\Users\TZK\Desktop\test_image\test13.png")
h, w, c = body_image.shape
# print(w, h, c)
image = cv2.resize(body_image, (int(w/2), int(h/2)))
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# classifier = cv2.CascadeClassifier(r"C:\Users\TZK\AppData\Local\Programs\Python\Python37\lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml")
# start = time.time()
# bodys = classifier.detectMultiScale(gray, 1.02, 3)
# end = time.time()
# for body in bodys:
#     x, y, w, h = body
#     cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 255), 1)
# cv2.imshow("body", image)
# print(end-start)
# cv2.waitKey()

detect_image = image
# detect_image = body_image
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# @jit(nopython=True)
def test():
    start = time.time()
    locations, weights = hog.detectMultiScale(detect_image, scale=1.09, winStride=(8, 8))
    end = time.time()
    print(end-start)
    return locations, weights
locations, weights = test()
print(locations, weights)
for body, w in zip(locations, weights):
    if w >0.9:
        color = (111, 222, 33)
    else:
        color = (255, 255, 255)
    x, y, w, h = body
    cv2.rectangle(detect_image, (x, y), (x+w, y+h), color, 2)
# print(end-start)
cv2.imshow("image", body_image)
cv2.imshow("image2", image)
# cv2.waitKey()

# features, hog_image = skhog(detect_image, orientations=11, transform_sqrt=0, block_norm="L1",pixels_per_cell=(8, 8), cells_per_block=(3, 3), visualize=True, feature_vector=True)
# print(features[:100])
# cv2.imshow("hog", hog_image)
# cv2.imshow("image", detect_image)
# # cv2.imshow("features", features)
# cv2.waitKey()

# if __name__ == "__main__":
#     start = time.time()
#     test()
#     print(time.time()-start)