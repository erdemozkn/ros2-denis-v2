cmake_minimum_required(VERSION 3.8)
project(object_detection)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(OpenCV REQUIRED)
find_package(trajectory_msgs REQUIRED)

add_executable(face_detection src/face_detection.cpp)

ament_target_dependencies(face_detection
  rclcpp
  sensor_msgs
  trajectory_msgs
  cv_bridge
  OpenCV
)

install(TARGETS face_detection
  DESTINATION lib/${PROJECT_NAME})

ament_package()
