#ifndef ROS2_COMPAT_HPP
#define ROS2_COMPAT_HPP

#include <cassert>
#include <cstdint>

#include <builtin_interfaces/msg/time.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <geometry_msgs/msg/quaternion.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <nav_msgs/msg/path.hpp>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/imu.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

#include <livox_ros_driver2/msg/custom_msg.hpp>

namespace sensor_msgs {
using Imu = msg::Imu;
using PointCloud2 = msg::PointCloud2;
using ImuConstPtr = msg::Imu::ConstSharedPtr;
}

namespace nav_msgs {
using Odometry = msg::Odometry;
using Path = msg::Path;
}

namespace geometry_msgs {
using PoseStamped = msg::PoseStamped;
using Quaternion = msg::Quaternion;
}

namespace livox_ros_driver {
using CustomMsg = livox_ros_driver2::msg::CustomMsg;
}

namespace ros2_compat {

inline rclcpp::Logger logger() {
  return rclcpp::get_logger("lidar_imu_init");
}

inline double to_sec(const builtin_interfaces::msg::Time &stamp) {
  return rclcpp::Time(stamp).seconds();
}

inline builtin_interfaces::msg::Time from_sec(double seconds) {
  builtin_interfaces::msg::Time stamp;
  const auto sec = static_cast<int64_t>(seconds);
  stamp.sec = static_cast<int32_t>(sec);
  stamp.nanosec = static_cast<uint32_t>((seconds - static_cast<double>(sec)) * 1e9);
  return stamp;
}

inline geometry_msgs::msg::Quaternion quaternion_from_rpy(double roll, double pitch, double yaw) {
  tf2::Quaternion quat;
  quat.setRPY(roll, pitch, yaw);
  return tf2::toMsg(quat);
}

}  // namespace ros2_compat

namespace ros {
class Time {
 public:
  Time() = default;
  explicit Time(const builtin_interfaces::msg::Time &stamp) : stamp_(stamp) {}

  double toSec() const {
    return ros2_compat::to_sec(stamp_);
  }

  Time fromSec(double seconds) const {
    return Time(ros2_compat::from_sec(seconds));
  }

  operator builtin_interfaces::msg::Time() const {
    return stamp_;
  }

 private:
  builtin_interfaces::msg::Time stamp_{};
};
}  // namespace ros

#define ROS_WARN(...) RCLCPP_WARN(ros2_compat::logger(), __VA_ARGS__)
#define ROS_INFO(...) RCLCPP_INFO(ros2_compat::logger(), __VA_ARGS__)
#define ROS_ERROR(...) RCLCPP_ERROR(ros2_compat::logger(), __VA_ARGS__)
#define ROS_ASSERT(condition) assert(condition)

#endif
