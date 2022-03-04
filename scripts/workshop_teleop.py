#!/usr/bin/env python3

import sys, select, termios, tty
import threading
import rospy
from std_msgs.msg import Float64

msg = """
Reading from the keyboard  and Publishing to bridge!
---------------------------
Control the motor:
range = [-1,1]

motor1:
w : up (+5%)
s : down (-5%)

motor2:
u : up (+5%)
j : down (-5%)

r : reset (0,0)
c : quit the program
"""


class PublishThread(threading.Thread):
    def __init__(self):
        super(PublishThread, self).__init__()
        self.publisherVel1 = rospy.Publisher('/pwm_percent1', Float64, queue_size = 1)
        self.publisherVel2 = rospy.Publisher('/pwm_percent2', Float64, queue_size = 1)
        self.pwm1 = 0.0
        self.pwm2 = 0.0
        self.done = False
        self.condition = threading.Condition()
        self.start()

    def update(self, pwm1 = 0, pwm2 = 0):
        self.condition.acquire()
        self.pwm1 = pwm1
        self.pwm2 = pwm2
        self.condition.notify()
        self.condition.release()
    
    def stop(self):
        self.done = True
        self.update()
        self.join()

    def run(self):
        while not self.done:
            self.condition.acquire()
            #10 Hz publish rate
            self.condition.wait(0.1)
            msg = Float64()
            msg.data = round(self.pwm1,2)
            self.publisherVel1.publish(msg)
            msg.data = round(self.pwm2,2)
            self.publisherVel2.publish(msg)
            self.condition.release()

def getKey(key_timeout = None):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key
    
def vels(pwm1,pwm2):
    return "currently: -motor1: \tspeed percent %s\t -motor2: \tspeed percent %s" % ((round(pwm1,2)),(round(pwm2,2)))

def limit_output(v):
    v = min(1,v)
    v = max(-1,v)
    return v

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('teleop')
    pub_thread = PublishThread()
    try:
        print(msg)
        pwm1 = 0.05
        pwm2 = -0.05
        rospy.loginfo(vels(pwm1,pwm2))
        pub_thread.update(0.1)
        status = 0
        while(1):
            key = getKey()
            print(key)
            if key == "w":
                pwm1 += 0.05

            elif key == "s":
                pwm1 -= 0.05
            
            elif key == "u":
                pwm2 += 0.05

            elif key == "j":
                pwm2 -= 0.05
            
            elif key == "r":
                pwm1 = pwm2 = 0.0
                
            elif key == "c":
                break

            pwm1 = limit_output(pwm1)
            pwm2 = limit_output(pwm2)
            rospy.loginfo(vels(pwm1,pwm2))
            if (status == 10):
                print(msg)
            status = (status + 1) % 15
            pub_thread.update(pwm1,pwm2)
            
    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()
        rospy.loginfo("hope you enjoy it! --NTU UAVIONICS CLUB")
