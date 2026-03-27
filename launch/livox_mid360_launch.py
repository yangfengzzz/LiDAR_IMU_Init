import os
import sys

sys.path.append(os.path.dirname(__file__))

from _li_init_launch import generate_li_init_launch_description


def generate_launch_description():
    return generate_li_init_launch_description(
        config_name="mid360.yaml",
        rviz_config_name="fast_lo.rviz",
        point_filter_num=2,
        cube_side_length=2000.0,
        include_mid360_driver=True,
        livox_config_path="/home/skysi/Desktop/3DNavPlanner/src/livox_ros_driver2/config/MID360_config.json",
    )
