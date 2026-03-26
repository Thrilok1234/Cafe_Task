#!/usr/bin/python3
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from ament_index_python.packages import get_package_share_directory, get_package_prefix

def generate_launch_description():
    pkg = get_package_share_directory('butlerbot')
    install_dir = get_package_prefix('butlerbot')
    gazebo_models_path = os.path.join(pkg, 'models')

    os.environ['GAZEBO_MODEL_PATH'] = os.environ.get('GAZEBO_MODEL_PATH','') + ':' + install_dir + '/share:' + gazebo_models_path
    os.environ['GAZEBO_PLUGIN_PATH'] = os.environ.get('GAZEBO_PLUGIN_PATH','') + ':' + install_dir + '/lib'

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value=os.path.join(pkg, 'worlds', 'cafe_new.world'),
            description='SDF world file'
        ),
        ExecuteProcess(
            cmd=['gazebo', os.path.join(pkg, 'worlds', 'cafe_new.world'), '-s', 'libgazebo_ros_factory.so', '-s', 'libgazebo_ros_init.so'],
            output='screen'
        )
    ])