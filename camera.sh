#!/bin/sh

ros2 run usb_cam usb_cam_node_exe --ros-args --params-file ./params.yaml --remap /image_raw:=/image_raw --remap /camera_info:=/camera_info
