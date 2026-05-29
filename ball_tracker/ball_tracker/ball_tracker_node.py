#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from cv_bridge import CvBridge
from builtin_interfaces.msg import Duration
import cv2
import numpy as np


class BallTrackerNode(Node):
    def __init__(self):
        super().__init__('ball_tracker')

        self.bridge = CvBridge()

        self.pan_angle = 0.0
        self.tilt_angle = 0.0

        self.declare_parameter('kp_pan', 0.8)
        self.declare_parameter('kp_tilt', 0.8)
        self.declare_parameter('pan_limit', 1.57)
        self.declare_parameter('tilt_limit', 0.6)
        self.declare_parameter('min_ball_area', 80.0)

        self.image_sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)

        self.head_pub = self.create_publisher(
            JointTrajectory, '/head_controller/joint_trajectory', 10)

        self.get_logger().info('Ball tracker started — detecting orange ball')

    def image_callback(self, msg: Image):
        kp_pan = self.get_parameter('kp_pan').value
        kp_tilt = self.get_parameter('kp_tilt').value
        pan_limit = self.get_parameter('pan_limit').value
        tilt_limit = self.get_parameter('tilt_limit').value
        min_area = self.get_parameter('min_ball_area').value

        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        h, w = frame.shape[:2]
        cx, cy = w / 2.0, h / 2.0

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, np.array([5, 120, 100]), np.array([25, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([170, 120, 100]), np.array([180, 255, 255]))
        mask = cv2.bitwise_or(mask1, mask2)

        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return

        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) < min_area:
            return

        M = cv2.moments(largest)
        if M['m00'] == 0:
            return

        ball_x = M['m10'] / M['m00']
        ball_y = M['m01'] / M['m00']

        err_x = (ball_x - cx) / cx
        err_y = (ball_y - cy) / cy

        self.pan_angle -= kp_pan * err_x * 0.04
        self.tilt_angle += kp_tilt * err_y * 0.04

        self.pan_angle = float(np.clip(self.pan_angle, -pan_limit, pan_limit))
        self.tilt_angle = float(np.clip(self.tilt_angle, -tilt_limit, tilt_limit))

        self._publish_command()

    def _publish_command(self):
        traj = JointTrajectory()
        traj.joint_names = ['head_base_neck_pan_link', 'head_base_tilt_pan_link']

        pt = JointTrajectoryPoint()
        pt.positions = [self.pan_angle, self.tilt_angle]
        pt.velocities = [0.0, 0.0]
        pt.time_from_start = Duration(sec=0, nanosec=100_000_000)

        traj.points = [pt]
        self.head_pub.publish(traj)


def main(args=None):
    rclpy.init(args=args)
    node = BallTrackerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
