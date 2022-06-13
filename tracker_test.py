from glob import glob
import cv2
import numpy as np

roi = None
drag_start = None
mouse_status = 0
tracking_start = False

# Mouse drag function
def onMouse(event, x, y, flags, param = None):
  global roi
  global drag_start
  global mouse_status
  global tracking_start
  
  if event == cv2.EVENT_LBUTTONDOWN:
    drag_start = (x, y)
    mouse_status = 1
    tracking_start = False
  elif event == cv2.EVENT_MOUSEMOVE:
    if flags == cv2.EVENT_FLAG_LBUTTON:
      min_X = min(x, drag_start[0])
      min_Y = min(y, drag_start[1])
      max_X = max(x, drag_start[0])
      max_Y = max(y, drag_start[1])
      roi = (min_X, min_Y, max_X, max_Y)
      mouse_status = 2
  elif event == cv2.EVENT_LBUTTONUP:
    mouse_status = 3

# Tracker generation function
def createTracker():
  tracker = cv2.TrackerCSRT_create()
  return tracker

# Screen Settings
cv2.namedWindow('tracking')
cv2.setMouseCallback('tracking', onMouse)

cap = cv2.VideoCapture(0)
tracker = None

# Tracking objects
while True:
  ret, img = cap.read()
  
  if mouse_status == 2:
    x1, y1, x2, y2 = roi
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0))
  if mouse_status == 3:
    mouse_status = 0
    track_box = (roi[0], roi[1], roi[2] - roi[0], roi[3] - roi[1])
    if tracker != None:
      del tracker
      
    tracker = createTracker()
    tracker.init(img, track_box)
    tracking_start = True
      
  if tracking_start:
    ret, track_box = tracker.update(img)
    if ret:
      x, y, w, h = track_box
      p1 = (int(x), int(y))
      p2 = (int(x + w), int(y + h))
      cv2.rectangle(img, p1, p2, (255, 0, 0), 2, 1)
  
  cv2.imshow('tracking', img)
  key = cv2.waitKey(10)
  if key == 27:
    break

cap.release()
cv2.destroyAllWindows()
