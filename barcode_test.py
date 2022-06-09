import argparse
from fnmatch import fnmatchcase
from pickle import TRUE
import cv2
import numpy as np
import os
import glob

from cv2 import sort

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
  th, dstx = cv2.threshold(dstx, 120, 200, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
  
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
  th, dsty = cv2.threshold(dsty, 120, 200, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
  
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
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    
  
  
  
  
if __name__ == '__main__':
  # Command Line Arguments Processing
  ap = argparse.ArgumentParser()
  ap.add_argument("-d", "--dataset", required=True, help="path to dataset folder")
  args = vars(ap.parse_args())

  dataset = args["dataset"]


  if (not os.path.isdir("results")):
    os.mkdir('results')

  verbose = True
  
  cap = cv2.VideoCapture(0)
  
  try:
    while (cap.isOpened()):
      ret, img = cap.read()
      
      # convert to gray scale images
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      
      # detect a barcode
      points = detectBarcode(gray, verbose)
  """
  # jpg file detection
  for imagePath in glob.glob(dataset + "/*.jpg"):
    print(imagePath, '처리중...')

    # convert to gray scale images
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect a barcode
    points = detectBarcode(gray, verbose)
    
    # To display the barcode area
    cv2.drawContours(image, [points], -1, (0, 255, 0), 3)
    
    loc1 = imagePath.rfind("\\")
    loc2 = imagePath.rfind(".")
    fname = 'results/' + imagePath[loc1+1:loc2] + '_res.jpg'
    cv2.imwrite(fname, image)
    
    if verbose:
      cv2.imshow("Image", image)
      cv2.waitKey(0)
  """