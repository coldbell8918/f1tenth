# F1 Tenth Simulator with TEB Local Planner 
### Rviz Mode  
[recording.webm](https://github.com/coldbell8918/f1tenth/assets/98142691/37c9daa1-5552-4675-9e5c-b6f6470fdc28)    
### Usage  
```
$ cd ~/catkin_ws/src  
$ git clone git clone https://github.com/coldbell8918/f1tenth.git
$ cd ..
$ catkin_make
$ source devel/setup.bash
$ roslaunch f1tenth_simulator simulator.launch  
$ roslaunch f1tenth_simulator racecar_navigation.launch  
$ rosrun f1tenth_simulator cmdvel_to_ackermann.py  
```
### Rotation Mode  
[rotation.webm](https://github.com/coldbell8918/f1tenth/assets/98142691/1abfb510-982f-4426-847f-2156b3843e78)  
### Usage  
```  
$ rosrun f1tenth_simulator goal.py  
```
