import cv2

img = cv2.imread(r"C:\Users\TZK\Pictures\Camera Roll\test2.jpg")
img = cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3)))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

his_img = cv2.equalizeHist(gray)
classifier = cv2.CascadeClassifier(r"C:\Users\TZK\AppData\Local\Programs\Python\Python37\lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml")
ret = classifier.detectMultiScale(img)
print(ret)
if ret is not None:
    for i in ret:
        x, y, w, h = i
        cv2.rectangle(img, (x, y), (x+w, y+h), (50, 200, 200), 2)
cv2.imshow("gray", gray)
cv2.imshow("img", img)
cv2.imshow("his_img", his_img)

cv2.waitKey()