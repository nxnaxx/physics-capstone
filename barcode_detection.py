import argparse
from fnmatch import fnmatchcase
import cv2
import os
import glob

def detectBarcode():
  
if __name__ == '__main__':
  # Command Line Arguments Processing
  ap = argparse.ArgumentParser()
  ap.add_argument("-d", "--dataset", required=True, help="path to dataset folder")
  args = vars(ap.parse_args())

  dataset = args["dataset"]


  if (not os.path.isdir("results")):
    os.mkdir('results')

  verbose = True
  
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