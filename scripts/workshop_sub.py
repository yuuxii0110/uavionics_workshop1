#!/usr/bin/env python3

import rospy 
import argparse
import RPi.GPIO as GPIO
from time import sleep
from std_msgs.msg import Float64

last_value = 0
direction = 0

def operate(value):
    if direction:
        pi_pwm2.ChangeDutyCycle(0)
        pi_pwm1.ChangeDutyCycle(value)
    else:
        pi_pwm1.ChangeDutyCycle(0)
        pi_pwm2.ChangeDutyCycle(value)

def send_signal(data):
    global last_value
    if data.data != last_value:
        if data.data > 0:
            direction = 1
        else:
            direction = 0

        rospy.loginfo(f"send duty cycle: {abs(data.data*100)} in direction {direction}")
        sleep(0.01)
        operate(abs(data.data)*100)
        last_value = data.data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pass the motor pin number')
    parser.add_argument('--in1', type=int, default=12, help='motor_IN1_pin')
    parser.add_argument('--in2', type=int, default=15, help='motor_IN2_pin')
    parser.add_argument('--topic', type=str, default='/pwm_percent1', help='corresponding ros topic')
    args = parser.parse_args()
    print('pin num, ', args.pin, ', topic_name: ', str(args.topic))
    motor_in1 = args.in1
    motor_in2 = args.in2
    topic = args.topic
    GPIO.setwarnings(False)			#disable warnings
    GPIO.setmode(GPIO.BOARD)		#set pin numbering system

    GPIO.setup(motor_in1,GPIO.OUT)  #initialize motor_pin
    GPIO.setup(motor_in2,GPIO.OUT)

    pi_pwm1 = GPIO.PWM(motor_in1,50)		#create PWM instance with frequency
    pi_pwm1.start(0)
    pi_pwm2 = GPIO.PWM(motor_in2,50)		
    pi_pwm2.start(0)	
    rospy.init_node('bridge_'+str(pi_pwm1), anonymous=False)
    rospy.loginfo("initialized bridge_"+str(pi_pwm1))
    sub1 = rospy.Subscriber(topic, Float64, send_signal, queue_size=1)
    rospy.spin()