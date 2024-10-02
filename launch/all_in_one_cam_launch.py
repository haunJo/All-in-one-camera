
import os
import sys

from pathlib import Path  # noqa: E402
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.actions import DeclareLaunchArgument
from launch.launch_description_sources import AnyLaunchDescriptionSource



def generate_launch_description():

    declare_arg = DeclareLaunchArgument(
        'display',
        default_value='false',
        description='Whether to run RViz2'
    )

    rviz_config_file = os.path.join(
        get_package_share_directory('yolov8_ros'),
        'rviz',
        'autoware_cam.rviz'
    )



    param_file = os.path.join(
        get_package_share_directory('usb_cam'),
        'config',
        'params_1.yaml'
    )
    proc_path = os.path.join(
        get_package_share_directory('image_proc')
    )
    
    include_sub_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(proc_path, 'launch', 'image_proc.launch.py')
        )
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        condition=IfCondition(LaunchConfiguration('display'))  # display 인자가 'true'일 때만 실행
    )

    xml_launch_file = os.path.join(
        get_package_share_directory('yolov8_bringup'),  # 다른 패키지 이름으로 변경
        'launch',
        'yolov8.launch.py'  # 실행할 XML 파일 이름
    )
   
    yolo_launch = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(xml_launch_file)
    )



    return LaunchDescription([
        yolo_launch,
        Node(
            package='usb_cam',
            namespace='usb_cam',
            executable='usb_cam_node_exe',
            name='usb_cam',
            parameters=[param_file],
            remappings = [('/usb_cam/image_raw', '/camera/rgb/image_raw'),
                          ('/usb_cam/camera_info', '/camera/rgb/camera_info')] 
        ) ,
        include_sub_launch, declare_arg,rviz_node]
    )
