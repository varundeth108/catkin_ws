#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import Int32
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler

class move2goal():
    # Write a function to get the odometry pose of the robot

    def __init__(self):
        rospy.init_node('move2goal')
        self.client = actionlib.SimpleActionClient('/move_base',MoveBaseAction)
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

    def movebase_client(self):
    #for pose in pose_seq:
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = -1
        goal.target_pose.pose.position.y = -1
        goal.target_pose.pose.orientation.w = 1.0
        rospy.loginfo("Sending goal pose to Action Server")
        self.client.send_goal(goal)
        #rospy.spin()

if __name__ == '__main__':
    try:
        move2goal()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation finished.")
