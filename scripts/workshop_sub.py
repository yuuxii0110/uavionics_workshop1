#!/usr/bin/env python3

import rospy 
import argparse
# import RPi.GPIO as GPIO
from time import sleep
from std_msgs.msg import Float64

last_value = 0

def send_signal(data):
    global last_value
    if data.data != last_value:
        # pi_pwm.ChangeDutyCycle(data.data*100)
        rospy.loginfo(f"send duty cycle: {data.data*100}")
        sleep(0.01)
        last_value = data.data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pass the motor pin number')
    parser.add_argument('--pin', type=int, default=12, help='motor_pin')
    parser.add_argument('--topic', type=str, default='/pwm_percent1', help='corresponding ros topic')
    args = parser.parse_args()
    print('pin num, ', args.pin, ', topic_name: ', str(args.topic))
    motor_pin = args.pin
    topic = args.topic
    # GPIO.setwarnings(False)			#disable warnings
    # GPIO.setmode(GPIO.BOARD)		#set pin numbering system
    # GPIO.setup(motor_pin,GPIO.OUT)
    # pi_pwm = GPIO.PWM(motor_pin,1000)		#create PWM instance with frequency
    # pi_pwm.start(0)	
    rospy.init_node('bridge_'+str(motor_pin), anonymous=False)
    rospy.loginfo("initialized bridge_"+str(motor_pin))
    sub1 = rospy.Subscriber(topic, Float64, send_signal, queue_size=1)
    rospy.spin()