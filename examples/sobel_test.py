import cv2

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
dstx = cv2.equalizeHist(dstx)

#cv2.imwrite('his_hori.jpg', dstx)

dstx = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

cv2.imwrite('thre_hori.jpg', dstx)

# Carry out a morphology transformation
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
