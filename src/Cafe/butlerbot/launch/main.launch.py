from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('butlerbot')

    # 1️⃣ Gazebo world
    world_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_share, 'launch', 'world.launch.py'))
    )

    # 2️⃣ Robot description + state publisher
    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_share, 'launch', 'rsp.launch.py'))
    )

    # 3️⃣ Spawn robot
    spawn_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_share, 'launch', 'desc.launch.py'))
    )
    
    slam_launch = TimerAction(
        period=10.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_share, 'launch', 'slam.launch.py'))
        )]
    )
    # 4️⃣ Map + AMCL (localization) - delayed 5s to ensure robot spawns
    localisation_launch = TimerAction(
        period=10.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_share, 'launch', 'localisation.launch.py'))
        )]
    )

    # 5️⃣ Nav2 pathplanning - delayed 8s to ensure map server and AMCL are ready
    pathplanning_launch = TimerAction(
        period=15.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_share, 'launch', 'pathplanning.launch.py'))
        )]
    )

    # 6️⃣ RViz - delayed 10s to wait for TFs
    rviz_launch = TimerAction(
        period=20.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_share, 'launch', 'rviz.launch.py'))
        )]
    )

    return LaunchDescription([
        world_launch,
        rsp_launch,
        spawn_launch,
        localisation_launch,
        pathplanning_launch,
        rviz_launch
    ])