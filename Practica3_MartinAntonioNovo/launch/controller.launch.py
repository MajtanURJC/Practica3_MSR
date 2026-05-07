from os.path import join
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node

from controller_manager.launch_utils import generate_load_controller_launch_description


def generate_launch_description():

    # -------- SIM TIME --------
    declare_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='use_sim_time simulation parameter'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')

    # -------- PACKAGE PATH --------
    pkg_share_folder = get_package_share_directory('practica3')
    arm_pkg_share_folder = get_package_share_directory('Robot_Rover_moveit_config')

    controllers_file = join(pkg_share_folder, 'config', 'rover_controllers.yaml')

    # -------- ROBOT DESCRIPTION (XACRO) --------
    xacro_file = os.path.join(pkg_share_folder, 'robots', 'robot.urdf.xacro')


    # -------- JOINT STATE BROADCASTER --------
    joint_state_broadcaster = GroupAction([
        generate_load_controller_launch_description(
            controller_name='joint_state_broadcaster',
            controller_params_file=controllers_file
        )
    ])

    # -------- BASE CONTROLLER --------
    base_controller = GroupAction([
        generate_load_controller_launch_description(
            controller_name='rover_base_control',
            controller_params_file=controllers_file
        )
    ])

    # Load arm controller
    arm_controller = GroupAction(
    [
    generate_load_controller_launch_description(
    controller_name='scara_controller',
    controller_params_file=join(
    arm_pkg_share_folder, 'config', 'ros2_controllers.yaml')
    )
    ],
    )
    # Load gripper controller
    gripper_controller = GroupAction(
    [
    generate_load_controller_launch_description(
    controller_name='gripper_controller',
    controller_params_file=join(
    arm_pkg_share_folder, 'config', 'ros2_controllers.yaml')
    )
    ],
    )

    # -------- LAUNCH DESCRIPTION --------
    return LaunchDescription([
        declare_sim_time,
        joint_state_broadcaster,
        base_controller,
        arm_controller,
        gripper_controller
    ])