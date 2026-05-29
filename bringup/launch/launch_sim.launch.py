import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

_desc_share = get_package_share_directory('description')
_gz_resource_path = os.path.dirname(_desc_share)  # .../install/description/share

_bringup_share = get_package_share_directory('bringup')
_gz_resource_path += ':' + _bringup_share  # exposes bringup/share/bringup/models/

os.environ['GZ_SIM_RESOURCE_PATH'] = (
    os.environ.get('GZ_SIM_RESOURCE_PATH', '') + ':' + _gz_resource_path
)

def generate_launch_description():
    pkg_denis_bringup = get_package_share_directory('bringup')

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(pkg_denis_bringup, 'launch', 'rsp.launch.py')
        ]),
        launch_arguments={
            'use_sim_time': 'true',
            'use_ros2_control': 'true'
        }.items()
    )

    default_world = os.path.join(pkg_denis_bringup, 'world', 'gazebo_urban_station.sdf')

    world = LaunchConfiguration('world')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='World to load'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ]),
        launch_arguments={
            'gz_args': LaunchConfiguration('gz_args', default=['-r -v 4 ', world]),
            'on_exit_shutdown': 'true'
        }.items()
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', '/robot_description',
            '-name', 'denis',
            '-x', '-1.0',
            '-y', '1.0',
            '-z', '5.23'
        ],
        output='screen'
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager-timeout", "35.0"],
        output='screen'
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller", "--controller-manager-timeout", "35.0"],
        output='screen'
    )

    head_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["head_controller", "--controller-manager-timeout", "35.0"],
        output='screen'
    )

    bridge_params = os.path.join(pkg_denis_bringup, 'config', 'bridge.yaml')
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=['--ros-args', '-p', f'config_file:={bridge_params}'],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # Spawn orange ball 2 m in front of the robot (robot is at x=-1, y=1)
    ball_sdf = os.path.join(pkg_denis_bringup, 'models', 'orange_ball', 'model.sdf')
    spawn_ball = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-file', ball_sdf,
            '-name', 'orange_ball',
            '-x', '1.5',
            '-y', '1.0',
            '-z', '5.5',
        ],
        output='screen'
    )

    ball_tracker = Node(
        package='ball_tracker',
        executable='ball_tracker_node',
        name='ball_tracker',
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        rsp,
        world_arg,
        gazebo,
        spawn_entity,
        ros_gz_bridge,
        TimerAction(
            period=6.0,
            actions=[
                joint_broad_spawner,
                diff_drive_spawner,
                head_controller_spawner,
                spawn_ball,
                ball_tracker,
            ]
        ),
    ])