import os
import sys

sys.path.append(os.path.dirname(__file__))

from _li_init_launch import generate_li_init_launch_description


def generate_launch_description():
    return generate_li_init_launch_description(
        config_name="pandar.yaml",
        rviz_config_name="spinning.rviz",
        point_filter_num=5,
        cube_side_length=2000.0,
    )
