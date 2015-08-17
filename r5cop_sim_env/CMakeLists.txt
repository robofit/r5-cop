cmake_minimum_required(VERSION 2.8.3)
project(r5cop_sim_env)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
  urdf
)

catkin_package()

include_directories(include ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS} ${SDFormat_INCLUDE_DIRS})
