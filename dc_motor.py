import RPi.GPIO as GPIO
import time
from rplidar import RPLidar

lidar = RPLidar('/dev/ttyUSB0')

A_I1_pwm = 16  # 속도 조절
A_I2 = 12  # 방향 조절
B_I1_pwm = 20
B_I2 = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(A_I1_pwm, GPIO.OUT)
GPIO.setup(A_I2, GPIO.OUT)
GPIO.setup(B_I1_pwm, GPIO.OUT)
GPIO.setup(B_I2, GPIO.OUT)

pwm_A = GPIO.PWM(A_I1_pwm, 1000.0)
pwm_B = GPIO.PWM(B_I1_pwm, 1000.0)
pwm_A.start(0.0)
pwm_B.start(0.0)

def getDistance():
  sumDistance = 0
  for i, scan in enumerate(lidar.iter_scans()):
    sumDistance += len(scan)
    if i > 4:
      break
  return sumDistance // 5

if __name__ == '__main__':
  try:
    while True:
      distance_value = getDistance()
      
      GPIO.output(A_I2, 0)
      pwm_A.ChangeDutyCycle(0.0)
      GPIO.output(B_I2, 0)
      pwm_B.ChangeDutyCycle(0.0)
      time.sleep(1.0)
      
      #Check whether the distance is 50 cm
      if distance_value > 150:      
          #Forward 1 seconds
          print ("Forward " + str(distance_value))
          GPIO.output(B_I2, 1)
          pwm_B.ChangeDutyCycle(50.0)
          GPIO.output(A_I2, False)
          pwm_A.ChangeDutyCycle(50.0)
          time.sleep(1)
      else:
          #Left 1 seconds
          print ("Left " + str(distance_value))
          GPIO.output(B_I2, 0)
          pwm_B.ChangeDutyCycle(0.0)
          GPIO.output(A_I2, 1)
          pwm_A.ChangeDutyCycle(50.0)
          time.sleep(1)
      
  except KeyboardInterrupt:
    print ("Terminate program by Keyboard Interrupt")
    GPIO.cleanup()

"""
try:
    while True:
        GPIO.output(A_I2, False)
        pwm_A.ChangeDutyCycle(0.0)
        GPIO.output(B_I2, False)  # 정지
        pwm_B.ChangeDutyCycle(0.0)
        time.sleep(1.0)
        GPIO.output(A_I2, True)
        pwm_A.ChangeDutyCycle(50.0)
        GPIO.output(B_I2, True)  # 전진 속도 50
        pwm_B.ChangeDutyCycle(50.0)
        time.sleep(1.0)
        GPIO.output(A_I2, True)
        pwm_A.ChangeDutyCycle(100.0)
        GPIO.output(B_I2, True)  # 정지
        pwm_B.ChangeDutyCycle(100.0)
        time.sleep(1.0)
        GPIO.output(A_I2, False)
        pwm_A.ChangeDutyCycle(50.0)
        GPIO.output(B_I2, False)  # 후진 속도 50
        pwm_B.ChangeDutyCycle(50.0)
        time.sleep(1.0)

except KeyboardInterrupt:
    pass
"""

pwm_A.ChangeDutyCycle(0.0)
pwm_B.ChangeDutyCycle(0.0)

pwm_A.stop()
pwm_B.stop()
GPIO.cleanup()