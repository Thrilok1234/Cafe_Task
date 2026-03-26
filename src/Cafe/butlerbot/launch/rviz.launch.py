import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg = get_package_share_directory('butlerbot')
    rviz_config_dir = os.path.join(pkg, 'rviz', 'nav_riz.rviz')  # Use your saved RViz config

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', rviz_config_dir]
    )
    return LaunchDescription([rviz_node])