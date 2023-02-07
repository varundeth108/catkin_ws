#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import Int32  # Added
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler

robot_x_1=0
robot_y_1=0
robot_x_2=0
robot_y_2=0
robot_x_3=0
robot_y_3=0

# Define the same quantitites in action server 
goal_x = -6
goal_y = 4



#def begin():
   # print("in odom")
    #rospy.Subscriber('tb3_0/odom', Odometry, callback)
    #print("out odom")


class neargoal():

    # Write a function to get the odometry pose of the robot
    def callback1(self,data):
        print(data.pose.pose)
        global robot_x_1, robot_y_1
        robot_x_1=data.pose.pose.position.x 
        robot_y_1=data.pose.pose.position.y
        print("Initial pose of turtlebot 1=",robot_x_1,robot_y_1)
        self.distance()

    def callback2(self,data):
        print(data.pose.pose)
        global robot_x_2, robot_y_2
        robot_x_2=data.pose.pose.position.x 
        robot_y_2=data.pose.pose.position.y 
        print("Initial pose of turtlebot 2=",robot_x_2,robot_y_2)
        self.distance()

    def callback3(self,data):
        print(data.pose.pose)
        global robot_x_3, robot_y_3
        robot_x_3=data.pose.pose.position.x 
        robot_y_3=data.pose.pose.position.y
        print("Initial pose of turtlebot 3=",robot_x_3,robot_y_3)
        self.distance()

    # Write a fucntion to calculate the euclidean distance
    def distance(self):
        global robot_x_1, robot_y_1, robot_x_2, robot_y_2, robot_x_3, robot_y_3 
        global distance_to_goal_tb3_01, distance_to_goal_tb3_02, distance_to_goal_tb3_03
        global goal_x, goal_y
        print("goal=",goal_x,goal_y)
        print("Robotpose=",robot_x_1,robot_y_1)
        print("Robotpose=",robot_x_2,robot_y_2)
        print("Robotpose=",robot_x_3,robot_y_3)
        distance_to_goal_tb3_01 = math.sqrt(math.pow((goal_x - robot_x_1), 2) + math.pow((goal_y - robot_y_1), 2))
        distance_to_goal_tb3_02 = math.sqrt(math.pow((goal_x - robot_x_2), 2) + math.pow((goal_y - robot_y_2), 2))
        distance_to_goal_tb3_03 = math.sqrt(math.pow((goal_x - robot_x_3), 2) + math.pow((goal_y - robot_y_3), 2))
        print("distance to first turtlebot =",distance_to_goal_tb3_01)  
        print("distance to second turtlebot =",distance_to_goal_tb3_02)
        print("distance to third turtlebot =",distance_to_goal_tb3_03)
        # Step 1: Compare the euclidean distance 
        if distance_to_goal_tb3_01<distance_to_goal_tb3_02 and distance_to_goal_tb3_01<distance_to_goal_tb3_03:
            self.robot = 0 
            print("First turtlebot is nearest")
            print('tb3_'+str(self.robot)+'/move_base')
            return self.robot
        elif distance_to_goal_tb3_02<distance_to_goal_tb3_01 and distance_to_goal_tb3_02<distance_to_goal_tb3_03: 
            self.robot = 1 
            print("Second turtlebot is nearest")
            print('tb3_'+str(self.robot)+'/move_base')
            return self.robot
        else :
            self.robot = 2
            print("Third turtlebot is nearest")
            print('tb3_'+str(self.robot)+'/move_base')
            return self.robot

    # Write a function to get the odometry pose of the robot
    def __init__(self):
        rospy.init_node('nearrobot')
        rospy.Subscriber('tb3_0/odom', Odometry, self.callback1)
        rospy.Subscriber('tb3_1/odom', Odometry, self.callback2)
        rospy.Subscriber('tb3_2/odom', Odometry, self.callback3)
        print("distance function")
        rate = rospy.Rate(10) # 10hz
        rate.sleep()
        self.robot=self.distance()
        pub = rospy.Publisher('/robot', Int32, queue_size=10)
        #rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            print("Near robot is publishing",self.robot)
            pub.publish(self.robot)
            rate.sleep()
        #rospy.spin()

if __name__ == '__main__':
    try:
        neargoal()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation finished.")