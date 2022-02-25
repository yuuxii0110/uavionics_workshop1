#!/usr/bin/env python3

import rospy 
# import RPi.GPIO as GPIO
from time import sleep
from std_msgs.msg import Float64

motor_pin = 12				# PWM pin connected to motor
# GPIO.setwarnings(False)			#disable warnings
# GPIO.setmode(GPIO.BOARD)		#set pin numbering system
# GPIO.setup(motor_pin,GPIO.OUT)
# pi_pwm = GPIO.PWM(motor_pin,1000)		#create PWM instance with frequency
# pi_pwm.start(0)	

def send_signal(data):
    # pi_pwm.ChangeDutyCycle(data.data*100)
    rospy.loginfo(f"send duty cycle: {data.data*100}")
    sleep(0.01)

if __name__ == "__main__":
    rospy.init_node('bridge', anonymous=False)
    rospy.loginfo("initialized bridge")
    sub = rospy.Subscriber('/pwm_percent', Float64, send_signal, queue_size=1)
    rospy.spin()