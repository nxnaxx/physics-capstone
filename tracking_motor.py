import RPi.GPIO as GPIO
import time

#Delay time
t = 0.01

#Setting GPIO
Motor_L_IN1 = 12
Motor_L_IN2 = 16
Motor_R_IN3 = 20
Motor_R_IN4 = 21
ENA = 23
ENB = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(Motor_L_IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Motor_L_IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Motor_R_IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Motor_R_IN4, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)

pwm_A = GPIO.PWM(ENA, 500)
pwm_B = GPIO.PWM(ENB, 500)
pwm_A.start(0)
pwm_B.start(0)

def brake():
   pwm_A.ChangeDutyCycle(10)
   pwm_B.ChangeDutyCycle(10)
   
   GPIO.output(Motor_L_IN1, False)
   GPIO.output(Motor_L_IN2, True)
   GPIO.output(Motor_R_IN3, False)
   GPIO.output(Motor_R_IN4, True)
   time.sleep(t)
   
   GPIO.output(Motor_L_IN1, False)
   GPIO.output(Motor_L_IN2, False)
   GPIO.output(Motor_R_IN3, False)
   GPIO.output(Motor_R_IN4, False)
   
   print("BRAKE")

def stop():
   pwm_A.ChangeDutyCycle(100)
   pwm_B.ChangeDutyCycle(100)
   
   GPIO.output(Motor_L_IN1, False)
   GPIO.output(Motor_L_IN2, False)
   GPIO.output(Motor_R_IN3, False)
   GPIO.output(Motor_R_IN4, False)
   
   print("STOP")

# Low speed
def forward_low():
   pwm_A.ChangeDutyCycle(40)
   pwm_B.ChangeDutyCycle(40)
   
   GPIO.output(Motor_L_IN1, True)
   GPIO.output(Motor_L_IN2, False)
   GPIO.output(Motor_R_IN3, True)
   GPIO.output(Motor_R_IN4, False)

   print("FORWARD_L")
   time.sleep(t)

def forward_fast():
   pwm_A.ChangeDutyCycle(65)
   pwm_B.ChangeDutyCycle(65)
   
   GPIO.output(Motor_L_IN1, True)
   GPIO.output(Motor_L_IN2, False)   
   GPIO.output(Motor_R_IN3, True)
   GPIO.output(Motor_R_IN4, False)

   print("FORWARD_F")
   time.sleep(t)

def reverse():
   pwm_A.ChangeDutyCycle(45)
   pwm_B.ChangeDutyCycle(45)
   
   GPIO.output(Motor_L_IN1, False)
   GPIO.output(Motor_L_IN2, True)
   GPIO.output(Motor_R_IN3, False)
   GPIO.output(Motor_R_IN4, True)

   print("REVERSE")
   time.sleep(t)

def turnRight():
   pwm_A.ChangeDutyCycle(50)
   pwm_B.ChangeDutyCycle(50)
   
   GPIO.output(Motor_L_IN1, False)
   GPIO.output(Motor_L_IN2, True)
   GPIO.output(Motor_R_IN3, True)
   GPIO.output(Motor_R_IN4, False)
   
   print ("TURN_R")
   time.sleep(t)

def turnLeft():
   pwm_A.ChangeDutyCycle(50)
   pwm_B.ChangeDutyCycle(50)
   
   GPIO.output(Motor_L_IN1, True)
   GPIO.output(Motor_L_IN2, False)
   GPIO.output(Motor_R_IN3, False)
   GPIO.output(Motor_R_IN4, True)

   print("TURN_L")
   time.sleep(t)

def cleanup():
   stop()  
   pwm_A.stop()
   pwm_B.stop()
   GPIO.cleanup()