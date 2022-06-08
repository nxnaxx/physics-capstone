import argparse
from fnmatch import fnmatchcase
import cv2
import os
import glob

def detectBarcode(img):
  # Calculate edge strength
  sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0)
  sobel_x = cv2.convertScaleAbs(sobel_x)
  sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1)
  sobel_y = cv2.convertScaleAbs(sobel_y)
  
  # Horizontal orientation; To detect barcode area
  dstx = cv2.subtract(sobel_x, sobel_y)
  # Carry out equalization and thresholding
  dstx = cv2.equalizeHist(dstx)
  dstx = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
  
  # Carry out a morphology transformation
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
  
  
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