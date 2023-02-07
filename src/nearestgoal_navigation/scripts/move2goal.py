#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import Int32  
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler

robot_x_1=0
robot_y_1=0
robot_x_2=0
robot_y_2=0
robot_x_3=0
robot_y_3=0

robot=0

class move2goal():
    # Write a function to get the odometry pose of the robot

    def callback(self,data):
        rospy.loginfo(rospy.get_caller_id() + "Nearesr robot is %d", data.data)
        global robot
        robot=data.data

    def __init__(self):
        rospy.init_node('move2goal')
        rospy.Subscriber('/robot', Int32, self.callback)
        rate = rospy.Rate(10) # 10hz
        rate.sleep()
        print("The robot is moving",robot)
        #print("tb3_'+str(self.robot)+'/move_base")
        self.client = actionlib.SimpleActionClient('tb3_'+str(robot)+'/move_base',MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        #wait = self.client.wait_for_server(rospy.Duration(5.0))
        wait = self.client.wait_for_server()
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
            return
        rospy.loginfo("Connected to move base server")
        rospy.loginfo("Starting goals achievements ...")
        self.movebase_client()

    

    def active_cb(self):
        rospy.loginfo("Goal pose is now being processed by the Action Server...")

    def feedback_cb(self, feedback):
        #rospy.loginfo("Feedback for goal "+str(self.goal_cnt)+": "+str(feedback))
        rospy.loginfo("Feedback for goal pose received")

    def done_cb(self, status, result):
       # Reference for terminal status values: http://docs.ros.org/diamondback/api/actionlib_msgs/html/msg/GoalStatus.html
        if status == 2:
            rospy.loginfo("Goal pose received a cancel request after it started executing, completed execution!")

        if status == 3:
            rospy.loginfo("Goal pose reached") 
            #next_goal = MoveBaseGoal()
            #next_goal.target_pose.header.frame_id = "map"
            #next_goal.target_pose.header.stamp = rospy.Time.now()
            #next_goal.target_pose.pose.position.x = 2
            #next_goal.target_pose.pose.position.y = 0
            #next_goal.target_pose.pose.orientation.w = 1.0
            #rospy.loginfo("Sending goal pose to Action Server")
            #self.client.send_goal(next_goal, self.done_cb, self.active_cb, self.feedback_cb) 
            #rospy.loginfo("Final goal pose reached!")
            #rospy.signal_shutdown("Final goal pose reached!")
            return

        if status == 4:
            rospy.loginfo("Goal pose was aborted by the Action Server")
            rospy.signal_shutdown("Goal pose aborted, shutting down!")
            return

        if status == 5:
            rospy.loginfo("Goal pose has been rejected by the Action Server")
            rospy.signal_shutdown("Goal pose rejected, shutting down!")
            return

        if status == 8:
            rospy.loginfo("Goal pose received a cancel request before it started executing, successfully cancelled!")

    def movebase_client(self):
    #for pose in pose_seq:   
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now() 
        goal.target_pose.pose.position.x = -6
        goal.target_pose.pose.position.y = 4
        goal.target_pose.pose.orientation.w = 1.0
        rospy.loginfo("Sending goal pose to Action Server")
        self.client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)
        #rospy.spin()

if __name__ == '__main__':
    try:
        move2goal()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation finished.")