import os
import random
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg = get_package_share_directory('butlerbot')

    position = [-3.0, 7.0, 0.2]
    orientation = [0.0, 0.0, -1.57]
    robot_base_name = "butler_bot"
    entity_name = robot_base_name + "-" + str(int(random.random()*100000))

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
            '-entity', entity_name,
            '-x', str(position[0]), '-y', str(position[1]), '-z', str(position[2]),
            '-R', str(orientation[0]), '-P', str(orientation[1]), '-Y', str(orientation[2]),
            '-topic', '/robot_description'
        ]
    )

    return LaunchDescription([spawn_robot])