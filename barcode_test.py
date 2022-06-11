import cv2
import numpy as np
import os
import pyzbar.pyzbar as pyzbar

def detectBarcode(img):
  # Calculate edge strength
  sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0)
  sobel_x = cv2.convertScaleAbs(sobel_x)
  sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1)
  sobel_y = cv2.convertScaleAbs(sobel_y)
  
  # Horizontal orientation; To detect barcode area
  dstx = cv2.subtract(sobel_x, sobel_y)
  # Carry out equalization and thresholding
  dstx = cv2.GaussianBlur(dstx, (7, 7), 0)
  th, dstx = cv2.threshold(dstx, 120, 200, cv2.THRESH_BINARY)
  
  # Carry out a morphology transformation
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (55, 11))
  dstx = cv2.morphologyEx(dstx, cv2.MORPH_CLOSE, kernel)
  dstx = cv2.erode(dstx, kernel, iterations=5)
  dstx = cv2.dilate(dstx, kernel, iterations=5)
  
  contours, hierarchy = cv2.findContours(dstx, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  if contours:
    max_X = sorted(contours, key=cv2.contourArea, reverse=True)[0]
  else:
    max_X = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])
  
  # Vertical orientation; To detect barcode area
  dsty = cv2.subtract(sobel_y, sobel_x)
  # Carry out equalization and thresholding
  dsty = cv2.GaussianBlur(dsty, (7, 7), 0)
  th, dsty = cv2.threshold(dsty, 120, 200, cv2.THRESH_BINARY)
  
  # Carry out a morphology transformation
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 55))
  dsty = cv2.morphologyEx(dsty, cv2.MORPH_CLOSE, kernel)
  dsty = cv2.erode(dsty, kernel, iterations=5)
  dsty = cv2.dilate(dsty, kernel, iterations=5)
  
  contours, hierarchy = cv2.findContours(dsty, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  if contours:
    max_Y = sorted(contours, key=cv2.contourArea, reverse=True)[0]
  else:
    max_Y = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])

  # To compare the size of the contours
  if (len(max_X) > len(max_Y)):
    rect = cv2.minAreaRect(max_X)
  else:
    rect = cv2.minAreaRect(max_Y)
  box = cv2.boxPoints(rect)
  box = np.int0(box)
  
  return box

if __name__ == '__main__':
  try:
    if (not os.path.isdir('result_img')):
      os.mkdir('result_img')
      
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 7)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    #img = cv2.imread('img/IMG_9807.jpg')
    
    while (cap.isOpened()):
      ret, img = cap.read()
      
      # convert to gray scale images
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      
      # detect a barcode
      points = detectBarcode(gray)
      
      result_img = cv2.drawContours(img, [points], -1, (0, 0, 255), 5)

      decoded = pyzbar.decode(gray)

      for d in decoded:
        barcode_data = d.data.decode("utf-8")
        cv2.putText(img, barcode_data, (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

      cv2.imshow('img', result_img)
      
      key = cv2.waitKey(1)
      if key == 27:
        break
      if key == ord('c'):
        cv2.imwrite('./result_img/' + barcode_data + '.jpg', result_img)
    
  except KeyboardInterrupt:
    pass

cap.release()
cv2.destroyAllWindows()