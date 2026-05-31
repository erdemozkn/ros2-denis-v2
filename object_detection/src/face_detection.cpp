#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "trajectory_msgs/msg/joint_trajectory.hpp"
#include "cv_bridge/cv_bridge.hpp"

class FaceDetectionNode : public rclcpp::Node
{
public:
  FaceDetectionNode() : rclcpp::Node("face_detection_node")
  {
    image_sub_ = this->create_subscription<sensor_msgs::msg::Image>("/camera/image_raw", 10, std::bind(&FaceDetectionNode::imageCallback, this, std::placeholders::_1));
    image_pub_ = this->create_publisher<sensor_msgs::msg::Image>("/gray_image", 10);
    trajectory_pub_ = this->create_publisher<trajectory_msgs::msg::JointTrajectory>("/head_controller/joint_trajectory", 10);
    RCLCPP_INFO(this->get_logger(), "Face detection and tracing has been started");
  }

private:
  void imageCallback(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    cv_bridge::CvImagePtr cv_ptr;
    cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    cv::Mat &frame = cv_ptr->image;
    cv::Mat gray;
    cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
    auto gray_msg = cv_bridge::CvImage(
                        msg->header,
                        sensor_msgs::image_encodings::MONO8,
                        gray)
                        .toImageMsg();

    image_pub_->publish(*gray_msg);
  }
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr image_sub_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr image_pub_;
  rclcpp::Publisher<trajectory_msgs::msg::JointTrajectory>::SharedPtr trajectory_pub_;
};

int main(int argc, char *argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FaceDetectionNode>());
  rclcpp::shutdown();
  return 0;
}