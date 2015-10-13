#!/usr/bin/env python

import rospy
import actionlib
import pr2_controllers_msgs.msg
from geometry_msgs.msg import PointStamped

def main():

    cl = actionlib.SimpleActionClient('/head_traj_controller/point_head_action', pr2_controllers_msgs.msg.PointHeadAction)
    cl.wait_for_server()
    goal = pr2_controllers_msgs.msg.PointHeadGoal()
        
    pt = PointStamped()
    pt.header.frame_id = "base_link"
    pt.point.x = 1.8
    pt.point.y = 0.0
    pt.point.z = 0.8
    
    goal.target = pt
    # goal.min_duration = rospy.Duration(3.0)
    goal.max_velocity = 1.0
    # goal.pointing_frame = "high_def_frame"
    goal.pointing_frame = "head_mount_kinect_rgb_link"
    goal.pointing_axis.x = 1
    goal.pointing_axis.y = 0
    goal.pointing_axis.z = 0
    
    print("point head: sending goal")
    cl.send_goal(goal)
    cl.wait_for_result()
    print("point head: finished")


if __name__ == "__main__":
    rospy.init_node('head_action_cl')
    main()
