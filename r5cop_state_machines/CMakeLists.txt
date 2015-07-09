cmake_minimum_required(VERSION 2.8.3)
project(r5cop_state_machines)

find_package(catkin REQUIRED COMPONENTS
  rospy
  tf
)


include_directories(
  ${catkin_INCLUDE_DIRS}
)

## Add folders to be run by python nosetests
# catkin_add_nosetests(test)
