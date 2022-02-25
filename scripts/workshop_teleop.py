#!/usr/bin/env python3

import sys, select, termios, tty
import threading
import rospy
from std_msgs.msg import Float64

msg = """
Reading from the keyboard  and Publishing to bridge!
---------------------------
Control the motor:
    
w : up (+10%)
s : down (-10%)
c : quit the program
"""


class PublishThread(threading.Thread):
    def __init__(self):
        super(PublishThread, self).__init__()
        self.publisherVel = rospy.Publisher('/pwm_percent', Float64, queue_size = 1)
        self.pwm = 0.0
        self.done = False
        self.condition = threading.Condition()
        self.start()

    def update(self, pwm = 0):
        self.condition.acquire()
        self.pwm = pwm
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
            msg.data = round(self.pwm,2)
            self.publisherVel.publish(msg)
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
    
def vels(pwm):
    return "currently:\tspeed percent %s" % (round(pwm,2))

def limit_output(v):
    v = min(1,v)
    v = max(0,v)
    return v

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('teleop')
    pub_thread = PublishThread()
    try:
        print(msg)
        pwm = 0.1
        rospy.loginfo(vels(pwm))
        pub_thread.update(0.1)
        status = 0
        while(1):
            key = getKey()
            if key == "w":
                pwm += 0.1

            elif key == "s":
                pwm -= 0.1

            elif key == "c":
                break

            pwm = limit_output(pwm)
            print(vels(pwm))
            if (status == 10):
                print(msg)
            status = (status + 1) % 15
            pub_thread.update(pwm)
            
    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()
        rospy.loginfo("hope you enjoy it!")