cmake_minimum_required(VERSION 2.8.3)
project(r5cop_state_machines)

find_package(catkin REQUIRED COMPONENTS
  rospy
  tf
  smach
  smach_ros
  actionlib
  actionlib_msgs
  moveit_commander
  moveit_msgs
  geometry_msgs
  roslaunch
)


include_directories(
  ${catkin_INCLUDE_DIRS}
)

## Add folders to be run by python nosetests
# catkin_add_nosetests(test)

#roslaunch_add_file_check(launch)
