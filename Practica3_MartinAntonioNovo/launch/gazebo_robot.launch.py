from os.path import join
from os import environ, pathsep

from ament_index_python.packages import (
    get_package_share_directory,
    get_package_prefix
)

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    SetEnvironmentVariable,
    IncludeLaunchDescription,
    OpaqueFunction
)

from launch.substitutions import (
    PathJoinSubstitution,
    LaunchConfiguration
)

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from moveit_configs_utils import MoveItConfigsBuilder


# ---------------------------
# Gazebo server + client
# ---------------------------
def start_gzserver(context, *args, **kwargs):

    pkg_path = get_package_share_directory('urjc_excavation_world')

    world_name = LaunchConfiguration('world_name').perform(context)
    world = join(pkg_path, 'worlds', world_name + '.world')

    # Gazebo server
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': ['-r -s -v 4 ', world]
        }.items()
    )

    # Gazebo client
    start_gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': [' -g ']
        }.items()
    )

    return [start_gazebo_server_cmd, start_gazebo_client_cmd]


# ---------------------------
# Model paths utility
# ---------------------------
def get_model_paths(packages_names):
    model_paths = ""

    for package_name in packages_names:
        if model_paths != "":
            model_paths += pathsep

        package_path = get_package_prefix(package_name)
        model_path = join(package_path, "share")
        model_paths += model_path

    if 'GZ_SIM_RESOURCE_PATH' in environ:
        model_paths += pathsep + environ['GZ_SIM_RESOURCE_PATH']

    return model_paths


# ---------------------------
# Main launch
# ---------------------------
def generate_launch_description():

    # MoveIt config 
    moveit_config = MoveItConfigsBuilder(
        "Robot_Rover",
        package_name="Robot_Rover_moveit_config"
    ).to_moveit_configs()

    # Sim time
    declare_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description="use_sim_time simulation parameter"
    )

    # World name (para Gazebo)
    declare_world_name = DeclareLaunchArgument(
        'world_name',
        default_value='small_house',
        description="Gazebo world file name (without .world)"
    )

    # ---------------------------
    # Model / resource paths
    # ---------------------------
    pkg_path = get_package_share_directory('practica3')

    model_path = join(pkg_path, 'models')

    resource_path = pkg_path

    model_paths = get_model_paths(['practica3'])

    # ---------------------------
    # Gazebo spawn robot
    # ---------------------------
    gazebo_spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-model", "Robot_rover",
            "-topic", "robot_description",
            "-use_sim_time", "True",
        ],
    )

    # Robot description (MoveIt / URDF publisher)
    robot_description_launcher = IncludeLaunchDescription(
        PathJoinSubstitution([
            FindPackageShare("Robot_Rover_moveit_config"),
            "launch",
            "rsp.launch.py"
        ])
    )

    # ---------------------------
    # RViz
    # ---------------------------
    rviz_config_file = PathJoinSubstitution([
        FindPackageShare("practica3"),
        "rviz",
        "robot.rviz"
    ])

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    # ---------------------------
    # ROS-Gazebo bridge
    # ---------------------------
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_ros_gz',
        output='screen',
        parameters=[{
            'config_file': join(pkg_path, 'config', 'rover_bridge.yaml'),
            'use_sim_time': True,
        }],
    )

    # Image bridge
    gz_image_bridge_node = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=[
            "/front_camera/image",
            "/arm_camera/image"
        ],
        output="screen",
        parameters=[{
            'use_sim_time': True,
            'camera.image.compressed.jpeg_quality': 75
        }],
    )

    # Twist stamper
    twist_stamped = Node(
        package="twist_stamper",
        executable="twist_stamper",
        name="twist_stamper",
        output="screen",
        parameters=[{
            "use_sim_time": True,
        }],
        remappings=[
            ('cmd_vel_out', '/rover_base_control/cmd_vel'),
            ('cmd_vel_in', '/cmd_vel')
        ],
    )

    # ---------------------------
    # Gazebo launch (server + client)
    # ---------------------------
    start_gazebo_server_cmd = OpaqueFunction(function=start_gzserver)

    # ---------------------------
    # Launch description
    # ---------------------------
    ld = LaunchDescription()

    ld.add_action(SetEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        model_paths
    ))

    ld.add_action(SetEnvironmentVariable(
        'GZ_SIM_MODEL_PATH',
        model_path
    ))

    ld.add_action(declare_sim_time)
    ld.add_action(declare_world_name)

    ld.add_action(robot_description_launcher)

    ld.add_action(start_gazebo_server_cmd)

    ld.add_action(bridge)
    ld.add_action(gz_image_bridge_node)

    ld.add_action(rviz_node)

    ld.add_action(gazebo_spawn_robot)

    ld.add_action(twist_stamped)

    return ld