#!/usr/bin/env python3
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry
import numpy as np
from std_srvs.srv import Trigger, TriggerRequest, TriggerResponse
from std_srvs.srv import Empty, EmptyRequest

class Dest():
    start=(0.0,8.7,1.57)
    middle=(-13.6,4.2,2.5)
    final=(0.0,0.0,0.0)

class MoveClient():

    def __init__(self):
        self.cnt=0 
        self.actionclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.odomsub = rospy.Subscriber('odom', Odometry, self.odom_callback)
        self.timer=rospy.Timer(rospy.Duration(5), self.clear_callback)
        self.start()


    def euler2quat(self):
        self.qx = np.sin(0) * np.cos(0) * np.cos(self.theta) - np.cos(0) * np.sin(0) * np.sin(self.theta)
        self.qy = np.cos(0) * np.sin(0) * np.cos(self.theta) + np.sin(0) * np.cos(0) * np.sin(self.theta)
        self.qz = np.cos(0) * np.cos(0) * np.sin(self.theta) - np.sin(0) * np.sin(0) * np.cos(self.theta)
        self.qw = np.cos(0) * np.cos(0) * np.cos(self.theta) + np.sin(0) * np.sin(0) * np.sin(self.theta)
        self.movebase_client()

    def movebase_client(self):
        self.actionclient.wait_for_server()
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = self.x
        goal.target_pose.pose.position.y = self.y
        goal.target_pose.pose.position.z = 0
        goal.target_pose.pose.orientation.x = self.qx
        goal.target_pose.pose.orientation.y = self.qy
        goal.target_pose.pose.orientation.z = self.qz
        goal.target_pose.pose.orientation.w = self.qw
        self.actionclient.send_goal(goal)
              
                    
    def odom_callback(self, data):
        self.robot_x = data.pose.pose.position.x
        self.robot_y = data.pose.pose.position.y
        distance = ((self.robot_x - self.x)**(2) + (self.robot_y - self.y)**(2))**(1/2)
        print('distance: ', distance)

        if self.cnt == 0:        
            if distance <= 0.5:
                self.cnt += 1
                self.middle()

        elif self.cnt == 1:        
            if distance <= 0.5:
                self.cnt += 1
                self.final()
        else:
            if distance <= 0.5:
                self.cnt = 0
                self.start()
            

    def clear_callback(self, timer):
        self.costmap_clear()

    def costmap_clear(self):
        try:    
            start_clear = rospy.ServiceProxy('move_base/clear_costmaps', Empty)
            return start_clear()

        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)

    def start(self):
        self.x=Dest.start[0]
        self.y=Dest.start[1]
        self.theta=Dest.start[2]
        self.euler2quat()
        

    def middle(self):
        self.x=Dest.middle[0]
        self.y=Dest.middle[1]
        self.theta=Dest.middle[2]
        self.euler2quat()
        

    def final(self):
        self.x=Dest.final[0]
        self.y=Dest.final[1]
        self.theta=Dest.final[2]
        self.euler2quat()
        


if __name__ == '__main__':
    rospy.init_node('movebase_client_py')
    cls_=MoveClient()
    rospy.spin()