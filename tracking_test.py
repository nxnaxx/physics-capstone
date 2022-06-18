import cv2
import numpy as np
import motor as motor
import sensor as sensor
import time

roi  = None
drag_start = None
mouse_status = 0
tracking_start = False

# Object setup function
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
      
# Screen setup
cv2.namedWindow('tracking')
cv2.setMouseCallback('tracking', onMouse)

cap = cv2.VideoCapture(0)
width, height = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#height, width = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
roi_mask = np.zeros((height, width), dtype=np.uint8)
term_crit = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 10, 1)

# Kalman Filter setup
q = 1e-5 # process noise covariance
r = 0.01 # measurement noise covariance
dt = 1

KF = cv2.KalmanFilter(4, 2, 0)
KF.transitionMatrix = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) # A
KF.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32) # H

i = 0
try:
  while True:
    ret, img = cap.read()

    img_copy = img.copy()
    
    # CamShift setup
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 60, 32), (180, 255, 255))
    
    if mouse_status == 2:
      x1, y1, x2, y2 = roi
      cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    if mouse_status == 3:
      mouse_status = 0
      x1, y1, x2, y2 = roi
      mask_roi = mask[y1:y2, x1:x2]
      hsv_roi = hsv[y1:y2, x1:x2]
      
      hist_roi = cv2.calcHist([hsv_roi], [0], mask_roi, [16], [0, 180])
      
      cv2.normalize(hist_roi, hist_roi, 0, 255, cv2.NORM_MINMAX)
      hist_copy = hist_roi.copy()
      cv2.normalize(hist_copy, hist_copy, 0.0, 1.0, cv2.NORM_MINMAX)
      track_window = (x1, y1, x2 - x1, y2 - y1)
      
      # Kalman Filter initialize
      KF.processNoiseCov = q * np.eye(4, dtype=np.float32) # Q
      KF.measurementNoiseCov = r * np.eye(2, dtype=np.float32) # R
      KF.errorCovPost = np.eye(4, dtype=np.float32) # P0 = I
      
      x, y, w, h = track_window
      cx = x + w / 2 # cx, cy; center coord.
      cy = y + h / 2
      KF.statePost = np.array([[cx], [cy], [0.], [0.]], dtype=np.float32) # x0
      
      tracking_start = True
      
    if tracking_start:
      predict = KF.predict()
      
      # CamShift Tracking
      backproj = cv2.calcBackProject([hsv], [0], hist_roi, [0, 180], 1)
      backproj &= mask
      
      track_box, track_window = cv2.CamShift(backproj, track_window, term_crit)

      if (i == 0):
        track_box_copy = track_box

      i += 1
      cv2.ellipse(img, track_box, (0, 0, 255), 2)
      cx, cy = track_box[0]
      cv2.circle(img, (round(cx), round(cy)), 5, (0, 0, 255), -1)
      
      # Kalman Filter correct
      z = np.array([[cx], [cy]], dtype=np.float32) # measurement vector
      estimate = KF.correct(z)
      estimate = np.int0(estimate)

      cx2, cy2 = estimate[0][0], estimate[1][0]
      track_box2 = ((float(cx2), float(cy2)), track_box[1], track_box[2])
      cv2.ellipse(img, track_box2, (0, 255, 0), 2)
      cv2.circle(img, (cx2, cy2), 5, (0, 255, 0), -1)

      # Motor movement
      center_X, center_Y = track_box[0][0], track_box[0][1]
      origin = track_box_copy[1][0]
      radius = track_box[1][0]

      
      obstacle = sensor.get_distance()

      if radius < origin + 50 and radius > origin - 30 and obstacle > 25:
        if center_X > width / 2 + 200:
          motor.turn_right()
        elif center_X < width / 2 - 200:
          motor.turn_left()
        else:
          motor.forward_low()
      elif obstacle <= 25:
        motor.back()
        time.sleep(0.3)
        motor.turn_right()
        if obstacle <= 15:
          motor.back()
          time.sleep(0.3)
          motor.turn_left()
      else:
        motor.stop()
      
    cv2.imshow('tracking', img)
    key = cv2.waitKey(10)
    if key == 27:
      break

except KeyboardInterrupt:
  pass

finally:
  cap.release()
  cv2.destroyAllWindows()
  motor.clean_up()

