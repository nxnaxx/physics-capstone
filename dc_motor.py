#from pickle import TRUE
#from trace import Trace
import RPi.GPIO as GPIO
import time

A_I1_pwm = 12  # 속도 조절
A_I2 = 16  # 방향 조절
B_I1_pwm = 20
B_I2 = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(A_I1_pwm, GPIO.OUT)
GPIO.setup(A_I2, GPIO.OUT)
GPIO.setup(B_I1_pwm, GPIO.OUT)
GPIO.setup(B_I2, GPIO.OUT)

pwmA = GPIO.PWM(A_I1_pwm, 1000.0)
pwmB = GPIO.PWM(B_I1_pwm, 1000.0)
pwmA.start(0.0)
pwmB.start(0.0)

try:
    while True:
        GPIO.output(A_I2, False)
        pwmA.ChangeDutyCycle(0.0)
        GPIO.output(B_I2, False)  # 정지
        pwmB.ChangeDutyCycle(0.0)
        time.sleep(1.0)
        GPIO.output(A_I2, True)
        pwmA.ChangeDutyCycle(0.0)
        GPIO.output(B_I2, True)  # 전진 속도 50
        pwmB.ChangeDutyCycle(0.0)
        time.sleep(1.0)
        GPIO.output(A_I2, True)
        pwmA.ChangeDutyCycle(100.0)
        GPIO.output(B_I2, True)  # 정지
        pwmB.ChangeDutyCycle(100.0)
        time.sleep(1.0)
        GPIO.output(A_I2, False)
        pwmA.ChangeDutyCycle(100.0)
        GPIO.output(B_I2, False)  # 후진 속도 50
        pwmB.ChangeDutyCycle(100.0)
        time.sleep(1.0)

except KeyboardInterrupt:
    pass

pwmA.ChangeDutyCycle(0.0)
pwmB.ChangeDutyCycle(0.0)

pwmA.stop()
pwmB.stop()
GPIO.cleanup()

'''
from gpiozero import Robot
from gpiozero import Motor
import time

dc_motor = Robot(left=(12, 16), right=(19, 26))

for num in range(4):
    dc_motor.forward(speed=1)
    time.sleep(1)

    dc_motor.stop()
    time.sleep(1)

    dc_motor.backward(speed=0.5)
    time.sleep(1)

dc_motor.stop()

'''
