import RPi.GPIO as GPIO                    
import time
from rplidar import RPLidar

lidar = RPLidar('/dev/ttyUSB0')                             

A_IN1 = 13                                
A_IN2 = 19                                  
ENA = 26
B_IN1 = 16                              
B_IN2 = 20
ENB = 21

def setPWM(EN):
  pwm = GPIO.PWM(EN, 100)
  pwm.start(0.0)
  pwm.ChangeDutyCycle(0.0)

def setPinConfig(IN1, IN2, EN):
  GPIO.setup(IN1, GPIO.OUT)
  GPIO.setup(IN2, GPIO.OUT)
  GPIO.setup(EN, GPIO.OUT)
  GPIO.output(EN, 0)
  
  setPWM(EN)
  #pwm = GPIO.PWM(EN, 100)
  #pwm.start(0.0)
  #pwm.ChangeDutyCycle(0.0)
  
def controlLeftMotor(IN1, IN2, pwm):
  GPIO.output(A_IN1, IN1)
  GPIO.output(A_IN2, IN2)
  A_pwm.ChangeDutyCycle(pwm)

def controlRightMotor(IN1, IN2, pwm):
  GPIO.output(B_IN1, IN1)
  GPIO.output(B_IN2, IN2)
  B_pwm.ChangeDutyCycle(pwm)


GPIO.setmode(GPIO.BCM)

# pin setting
A_pwm = setPinConfig(A_IN1, A_IN2, ENA)
B_pwm = setPinConfig(B_IN1, B_IN2, ENB)

def getDistance():
  while True:
    distance = enumerate(lidar.iter_scans())
    return distance

if __name__ == '__main__':
  try:
    while True:
      distance_value = getDistance()
      
      if distance_value > 120:
        controlLeftMotor(1, 0, 70)
        controlRightMotor(1, 0, 70)
        time.sleep(1)
      else:
        controlRightMotor(0, 0, 70)
        controlLeftMotor(1, 0, 70)
        time.sleep(1)
    
  except KeyboardInterrupt:
    GPIO.cleanup()