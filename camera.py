#import cv2
from cv2 import cv2

cap = cv2.VideoCapture(0)
if cap.isOpened():
    print('width:', cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print('height:', cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print('fps:', cap.get(cv2.CAP_PROP_FPS))

while cap.isOpened():
    ret, img = cap.read()

    if ret:
        cv2.imshow('Video Capture', img)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()
