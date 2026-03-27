import os

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _flatten_params(prefix, value, output):
    if isinstance(value, dict):
        for key, child in value.items():
            next_prefix = f"{prefix}.{key}" if prefix else key
            _flatten_params(next_prefix, child, output)
    else:
        output[prefix] = value


def _load_params(config_name, point_filter_num, cube_side_length, max_iteration):
    package_share = get_package_share_directory("lidar_imu_init")
    config_path = os.path.join(package_share, "config", config_name)
    with open(config_path, "r", encoding="utf-8") as handle:
        raw_params = yaml.safe_load(handle) or {}

    params = {}
    _flatten_params("", raw_params, params)
    float_keys = {
        "preprocess.blind",
        "initialization.mean_acc_norm",
        "initialization.online_refine_time",
        "initialization.data_accum_length",
        "mapping.filter_size_surf",
        "mapping.filter_size_map",
        "mapping.gyr_cov",
        "mapping.acc_cov",
        "mapping.b_acc_cov",
        "mapping.b_gyr_cov",
        "mapping.det_range",
    }
    for key in float_keys:
        if key in params:
            params[key] = float(params[key])
    params["point_filter_num"] = point_filter_num
    params["max_iteration"] = max_iteration
    params["cube_side_length"] = float(cube_side_length)
    return params


def generate_li_init_launch_description(
    *,
    config_name,
    rviz_config_name,
    point_filter_num,
    cube_side_length,
    max_iteration=5,
    include_mid360_driver=False,
    livox_config_path=None,
):
    def launch_setup(_context):
        package_share = get_package_share_directory("lidar_imu_init")
        params = _load_params(config_name, point_filter_num, cube_side_length, max_iteration)
        actions = []

        if include_mid360_driver:
            driver_parameters = [
                {"xfer_format": 1},
                {"multi_topic": 0},
                {"data_src": 0},
                {"publish_freq": 10.0},
                {"output_data_type": 0},
                {"frame_id": "livox_frame"},
                {"user_config_path": LaunchConfiguration("livox_config_path")},
            ]
            actions.append(
                Node(
                    package="livox_ros_driver2",
                    executable="livox_ros_driver2_node",
                    name="livox_lidar_publisher",
                    output="screen",
                    parameters=driver_parameters,
                    condition=IfCondition(LaunchConfiguration("start_driver")),
                )
            )

        actions.append(
            Node(
                package="lidar_imu_init",
                executable="li_init",
                name="laserMapping",
                output="screen",
                parameters=[params],
            )
        )

        actions.append(
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=["-d", os.path.join(package_share, "rviz_cfg", rviz_config_name)],
                condition=IfCondition(LaunchConfiguration("rviz")),
            )
        )
        return actions

    declared_arguments = [
        DeclareLaunchArgument("rviz", default_value="true"),
    ]
    if include_mid360_driver:
        declared_arguments.append(DeclareLaunchArgument("start_driver", default_value="true"))
        declared_arguments.append(
            DeclareLaunchArgument("livox_config_path", default_value=livox_config_path or "")
        )

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])
