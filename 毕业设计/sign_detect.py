import time
import cv2
import numpy as np
import img_pre

cap = cv2.VideoCapture(0)
ret = 1
font = cv2.FONT_HERSHEY_COMPLEX
while ret:

    ret, img = cap.read()
    # print(img.shape)
    # img : np.ndarray = cv2.imread(r"G:\image-dataset\raw\fog.png")
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_e = cv2.equalizeHist(gray)
    # img = cv2.resize(img, (640, 860))
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(img_hsv, np.array([0, 46, 46]), np.array([10,255,255]))
    mask2 = cv2.inRange(img_hsv, np.array([156, 46, 46]), np.array([180,255,255]))
    mask = mask1 + mask2
    mask_blur = cv2.medianBlur(mask, ksize=9)

    # kernel_1 = np.ones((3, 3), np.uint8)
    # kernel_2 = np.ones((7, 7), np.uint8)
    # erode = cv2.erode(mask_blur, kernel_1)
    # dilate = cv2.dilate(erode, kernel_2)

    w, h = np.shape(img)[:2]
    # cv2.floodFill(dilate, np.zeros((w+2, h+2), np.uint8), (0, 0), (0, 0, 0))
    # contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_new = np.zeros([w, h], np.uint8)
    # for contour in contours:
    #     cv2.drawContours(img_new, [contour], -1, (255, 255, 255), -1)
    # img_edge2 = cv2.Canny(mask, 50, 150)
    img_edge = cv2.Canny(mask_blur, 50, 100)
    hough = cv2.HoughCircles(img_edge, cv2.HOUGH_GRADIENT, minDist=50, dp=1, param2=30, minRadius=33, maxRadius=100)
    text_x, text_y = 0, 0
    new_img = None
    try:
        for i in hough[0]:

            # print(i)
            x = int(i[0])-int(i[2])-8
            y = int(i[1])-int(i[2])-8
            w = 2*int(i[2])+8
            h = 2*int(i[2])+8
            new_img = img[y:y+h, x:x+w] 
            text_x, text_y = x, y
            
            # cv2.circle(img, (i[0], i[1]), int(i[2])+8, (0, 200, 150), 2)           
    except:
        pass
    if new_img is not None:
        y, x = new_img.shape[:2]
        if (x and y) > 64:
            time1 = time.time()
            result = img_pre.recognition(new_img)
            cv2.putText(img, result[0], org=(text_x, text_y), fontFace=font, fontScale=1, color=(100, 200, 50), thickness=1)
            print(time.time()-time1)
            cv2.imshow("new", new_img)
    cv2.imshow("img", img)

    key = cv2.waitKey(25)
    if key&0xFF == ord("q"):
        break
