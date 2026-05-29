# Human-Aware Differential Drive Robot with Navigation

## Project Overview

This project is a small autonomous robot with a differential drive system. The robot has two main wheels and one caster wheel for balance. It also includes a movable neck and head system with eyes. The main goal of the project is to create a robot that can detect a human face and turn its head toward the person.

The robot is designed for learning and experimentation in robotics, ROS 2, computer vision, and motion control.

## Main Features

* Differential drive movement
* Two-wheel drive with caster wheel support
* Movable neck system
* Pan and tilt head movement
* Human face detection
* Eye direction control
* Real-time tracking behavior
* ROS 2 based software architecture

## Technologies Used

* ROS 2
* URDF / Xacro
* Gazebo
* Python
* OpenCV
* Linux

## Robot Design

The robot uses a differential drive mechanism. The left and right wheels are controlled independently, which allows the robot to move forward, backward, and rotate.

A caster wheel is placed at the back side of the robot to keep balance during movement.

The head system has a neck with two axes:

* Pan movement for left and right rotation
* Tilt movement for up and down rotation

This structure helps the robot follow a detected person naturally.

## Face Tracking System

The robot uses a camera to detect human faces. After detection, the system calculates the position of the face inside the camera frame.

If the face moves:

* The neck pan joint rotates left or right
* The tilt joint moves up or down
* The robot tries to keep the face in the center of the view

The goal is to make the interaction feel more natural.

## Project Goals

The main goals of this project are:

* Learning ROS 2 in a practical way
* Understanding robot kinematics
* Building a custom URDF robot model
* Combining computer vision with robot control
* Creating a simple human-robot interaction system

## Future Improvements

Possible future updates:

* Voice interaction
* Object tracking
* SLAM and autonomous navigation
* Better eye animations
* AI based human interaction
* Battery management system

## Current Status

The project is still in the development phase. Right now, the robot is being developed and tested in simulation. After the simulation side becomes stable, the physical parts will be combined and assembled. Some of the hardware parts are already available. Mechanical design, robot modeling, and motion control systems are still being improved.

## Author

Erdem Özkan
