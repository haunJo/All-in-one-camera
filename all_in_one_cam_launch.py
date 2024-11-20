
import os
import sys
import yaml


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
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
# YAML 파일 경로
    yaml_file = os.path.join('config', 'all_in_one.yaml')

# YAML 파일 읽기
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)  # 파일을 파싱하여 파이썬 객체로 변환

# 출력하여 확인
    print(config)

# 'usb_cam' 내의 'ros__parameters'에서 값을 가져오기
    usb_cam_config = config.get('usb_cam', {}).get('ros__parameters', {})
    display = usb_cam_config.get('display', False)
    rectify = usb_cam_config.get('rectify', False)
    use_simulator = usb_cam_config.get('use_simulator', False)
    
    rviz_config_file = os.path.join(
        'config',
        'yolo.rviz'
    )



    camera_param = os.path.join(
        get_package_share_directory('usb_cam'),
        'config',
        'params_1.yaml'
    )
    proc_path = os.path.join(
        get_package_share_directory('image_proc'),
        'launch',
        'image_proc.launch.py'
    )

    xml_launch_file = os.path.join(
        get_package_share_directory('yolo_bringup'),  # 다른 패키지 이름으로 변경
        'launch',
        'yolo.launch.py'  # 실행할 XML 파일 이름
    )
    
    raw_topic = [('/usb_cam/image_raw', '/camera/rgb/image_raw'),
                          ('/usb_cam/camera_info', '/camera/rgb/camera_info')] 
    rectify_topic = [('/usb_cam/image_raw', '/image_color'),
                          ('/usb_cam/camera_info', '/camera_info')] 

    # 카메라 실행
    camera_node = Node(
            package='usb_cam',
            namespace='usb_cam',
            executable='usb_cam_node_exe',
            name='usb_cam',
            parameters=[camera_param],
            remappings = rectify_topic if rectify else raw_topic
        )
    
    # RVIZ 실행
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    # 이미지 전처리 실행
    composable_nodes = [
        ComposableNode(
            package='image_proc',
            plugin='image_proc::DebayerNode',
            name='debayer_node',
        ),

        ComposableNode(
            package='image_proc',
            plugin='image_proc::RectifyNode',
            name='rectify_color_node',
            # Remap subscribers and publishers
            remappings=[
                ('image', 'image_color'),
                ('image_rect', '/camera/rgb/image_raw')
            ],
        )
    ]

    image_processing = ComposableNodeContainer(
        name='image_proc_container',
        namespace='image_proc_container',
        package='rclcpp_components',  # This package contains the container
        executable='component_container',
        composable_node_descriptions=composable_nodes,
        output='screen',
    )
    # YOLO 실행

    if use_simulator:
        yolo_image_topic = "/sensing/camera/traffic_light/image_raw"
    else:
        yolo_image_topic = "/camera/rgb/image_raw"



    yolo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(xml_launch_file),
        launch_arguments = {
        'input_image_topic': yolo_image_topic
        }.items()
    )
    
    excutes = [
        yolo_launch
        ]
    
    if not use_simulator:
        excutes.append(camera_node)

    if rectify:
        excutes.append(image_processing)
    if display:
        excutes.append(rviz_node)

    return LaunchDescription(excutes)
