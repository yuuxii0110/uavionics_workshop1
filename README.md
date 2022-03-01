# uavionics_workshop1 (Control propeller with ROS and Raspberry PI I/O pin)

__This repository assumes readers have a complete ROS1 environment, if you haven't done so, please follow the ros installation guide which matches your OS version: http://wiki.ros.org/ROS/Installation"__

1) Create and initialize catkin workspace (skip if you have a workspace)
  open terminal in home directory
  ```
  mkdir catkin_ws
  mkdir catkin_ws/src
  cd catkin_ws
  cd src
  catkin_init_workspace
  ```
  
  After that, compile your workspace
  ```
  catkin_make
  ```
  
2) Clone Repo from github and compile
  Then, in the terminal, proceed to the src directory and clone this repo
  ```
  cd ~/catkin_ws/src
  git clone https://github.com/yuuxii0110/uavionics_workshop1.git
  ```
  
  Now you have done cloning all the resources from github, next we have to compile all the codes:
  ```
  cd ~/catkin_ws
  catkin_make
  ```
  
3) Run everything!
  First, initialize the ros master in a new terminal
  ```
  roscore
  ```
  
  Makesure you have make the python codes executable:
  ```
  chmod +x ~/catkin_ws/src/uavionics_workshop1/scripts/workshop_sub.py ~/catkin_ws/src/uavionics_workshop1/scripts/workshop_teleop.py
  ```
  
  Then, open another terminal, source the setup.bash file in your workspace before run the teleop code.
  ```
  source ~/catkin_ws/devel/setup.bash
  rosrun uavionics_workshop1 workshop_teleop.py
  ```
  
  Now the terminal will looks like below:
  
  
  ![alt test](https://github.com/yuuxii0110/uavionics_workshop1/blob/main/images/teleop_terminal.png?raw=true)
  
  Lastly, open another terminal and do the similar thing with subscriber code.
  ```
  source ~/catkin_ws/devel/setup.bash
  rosrun uavionics_workshop1 workshop_sub.py
  ```
  
  Check if the terminal shows the message:
  ![alt test](https://github.com/yuuxii0110/uavionics_workshop1/blob/main/images/sub_terminal.png?raw=true)
  
  If you wish to control both motors simultaneously, open another terminal and type
  ```
  source ~/catkin_ws/devel/setup.bash
  rosrun uavionics_workshop1 workshop_sub.py --pin <motor_pin> --topic /pwm_percent2
  ```
  __Note: replace the motor_pin to the pin_num on the raspberry PI that attached to the motor2__
  
  Now go to the teleop terminal to control a motor speed by pressing "w" (increase speed), "s" (decrease speed)
  To quit the program, press "c"
  
  Observe the rosnode and rostopic by opening a new terminal and type:
  ```
  rqt_graph
  ```
  ![alt test](https://github.com/yuuxii0110/uavionics_workshop1/blob/main/images/rosgraph2.png?raw=true)
  
  
  
 
  

  
