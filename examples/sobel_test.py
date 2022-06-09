import cv2
import numpy as np

img = cv2.imread('../img/IMG_9736.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
sobel_x = cv2.convertScaleAbs(sobel_x)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
sobel_y = cv2.convertScaleAbs(sobel_y)

#cv2.imwrite('sobel_hori.jpg', dstx)
#cv2.imwrite('sobel_ver.jpg', dsty)

# Horizontal orientation; To detect barcode area
dstx = cv2.subtract(sobel_x, sobel_y)
# Carry out equalization and thresholding
dstx = cv2.GaussianBlur(dstx, (7, 7), 0)
th, dstx = cv2.threshold(dstx, 120, 200, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Carry out a morphology transformation
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (55, 11))
dstx = cv2.morphologyEx(dstx, cv2.MORPH_CLOSE, kernel)
dstx = cv2.erode(dstx, kernel, iterations=5)
dstx = cv2.dilate(dstx, kernel, iterations=5)

(contours, hierarchy) = cv2.findContours(dstx, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if not contours:
  max_X = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])
else:
  max_X = sorted(contours, key=cv2.contourArea, reverse=True)[0]

rect = cv2.minAreaRect(max_X)
box = cv2.boxPoints(rect)
box = np.int0(box)
#cv2.drawContours(dstx, [box], 0, (0, 255, 0), 3)
#cv2.rectangle(dstx, (box[2][0], box[2][1]), (box[0][0], box[0][1]), (0, 255, 0), 2)

#cv2.imwrite('ero_hori.jpg', dstx)
print(box[-1])