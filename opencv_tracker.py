import cv2
import numpy as np
import tracking_motor as motor

roi  = None
drag_start = None
mouse_status = 0
tracking_start = False

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
      xmin = min(x, drag_start[0])
      ymin = min(y, drag_start[1])
      xmax = max(x, drag_start[0])
      ymax = max(y, drag_start[1])
      roi = (xmin, ymin, xmax, ymax)
      mouse_status = 2
  elif event == cv2.EVENT_LBUTTONUP:
      mouse_status = 3

def createTracker(track_type=0):
  if track_type == 0:
    tracker = cv2.TrackerCSRT_create()
  elif track_type == 1:
    tracker = cv2.TrackerKCF_create()
  elif track_type == 2:
    tracker = cv2.TrackerMIL_create()
  else:
    tracker = cv2.TrackerGOTURN_create()   
  return tracker

      
cv2.namedWindow('tracking')
cv2.setMouseCallback('tracking', onMouse)

cap = cv2.VideoCapture(0)
if (not cap.isOpened()):
  print('Error opening video')
height, width = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
tracker = None
  
#4
try:
  while True:
    ret, frame = cap.read()
    if not ret: break

    if mouse_status == 2:
      x1, y1, x2, y2 = roi
      cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  
    if mouse_status == 3:
      print('initialize....')
      mouse_status = 0
      track_box = (roi[0], roi[1], roi[2]-roi[0], roi[3]-roi[1])
      
      if tracker != None:
        del tracker

        tracker = createTracker()
        tracker.init(frame, track_box)
        tracking_start = True
      
    if tracking_start:
      ret, track_box = tracker.update(frame)
      if ret:
        x, y, w, h =  track_box
        p1 = (int(x), int(y))
        p2 = (int(x + w), int(y + h))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    
      try:
        if int(w) < 25 and int(w) > 5 :   

          if p1[0] > Frame_Width/2 + 55 :  #turnRight_Area Set
            motor.turnRight()
            
          elif p1[0] < Frame_Width/2 - 55 : #turnLeft_Area Set
            motor.turnLeft()
            
          else:
            motor.forward_fast()                #Fast Run
                            
        elif int(x) < 45 and int(x) > 25 :

          if p1[0] > Frame_Width/2 + 55 :
            motor.turnRight()
            
          elif p1[0] < Frame_Width/2 - 55 :
            motor.turnLeft()
            
          else:
            motor.forward_low()               #Low Run
        
        elif int(x) > 65:
          motor.reverse()
                        
        else:
          motor.brake()
                          
      except:
        pass

    else:
      motor.stop()
      cv2.imshow('tracking', frame)
      key = cv2.waitKey(200)
      
      if key == 27:
        break

finally:
  if cap.isOpened():
    cap.release()
    
  cv2.destroyAllWindows()