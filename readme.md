# ALL-in-one-camera-ros2

> End-to-End Autononous Vehicle Perception framework based on ROS2 humble

# Requirements
- ROS2 humble
- OpenCV4
- python3


# 1. installation


```bash
$ git clone --recursive https://github.com/haunjo/All-in-one-camera-ROS2.git
```

```bash
$ cd src/yolo_ros
$ pip3 install requirements.txt
```

```bash
$ rosdep update
$ rosdep install --from-paths src -y --ignore-src
$ colcon build
$ source install/setup.bash
```

# 2. launching

```bash
ros2 launch all_in_one_cam_launch.py
```


# 3. Conponents
## usb_cam

This is a camera driver

## yolo_ros

This is a real-time object detection library