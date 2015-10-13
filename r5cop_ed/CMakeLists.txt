cmake_minimum_required(VERSION 2.8.3)
project(r5cop_ed)

find_package(catkin REQUIRED COMPONENTS
  ed
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)
