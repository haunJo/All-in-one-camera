# ROS2 usb_cam node 가이드

> ROS2 humble 환경에서 USB 카메라를 운용하기 위한 ros-driver인 `usb_cam` 을 사용하는 과정을 설명합니다.
> 

<aside>
💡 기본 사양

- 운영 체제 : Ubuntu 22.04
- ROS2 버전 : humble
- 사전 준비 사항
 - USB 카메라
 - 컴퓨팅 환경

</aside>

## 개요

---

이 ROS2 공식 지원 패키지는 **USB 카메라**를 연결하여 **ROS2 humble 환경에서 운용**하는 기능을 제공합니다.  https://github.com/ros-drivers/usb_cam 에서 **세부 내용**을 확인할 수 있습니다. 필자는 **Ubuntu 22.04** 환경과 **Tier4 C1 camera**를 사용합니다.

## 시나리오 소개

---

이 문서에서는 우분투 OS에서 USB 3.0 카메라를 연결하고,  ROS2 서버에 접속한 뒤  `usb_cam` 을 실행해 카메라에서 **이미지를 수집**하여 **수신한 이미지를 조회**한 뒤, 카메라의 **파라미터를 조정**하는 방법을 소개합니다. 주요 시나리오는 다음과 같습니다.

- `usb_cam` 노드의 기능 안내
- `usb_cam` 이미지 토픽 조회 방법
- `usb_cam` 파라미터 조정을 위한 `params.yaml` 과 `camera_info.yaml` 작성 방법

## 사전 작업

---

- 우분투 환경 구축
- ROS2 humble 설치
- `usb_cam` 설치
    
    ```bash
    sudo apt-get install ros-<ros2-distro>-usb-cam
    
    # ros2-distro == humble
    ```
    

## Step 1. 실행

---

`usb_cam_node` 는 default 설정으로 실행할 수 있지만, 특정 파라미터를 실행 시 **명령어에 argument로 입력**하거나 **파라미터 파일을 로딩**하여 입력할 수 있습니다. 이를 위해 `usb_cam/config/params.yaml` 파일에는 파라미터 파일을 작성하기 위한 가이드가 제공되어 있습니다. 사용자는 이 파일을 **목적에 맞게 내용을 재구성**하여 사용할 수 있습니다.

1. Default 설정으로 실행 시
    
    ```bash
    # run the executable with default settings (without params file)
    ros2 run usb_cam usb_cam_node_exe
    ```
    
2. 파라미터 파일을 argument로 주어 실행 시
    
    ```bash
    #run the executable while passing in parameters via a yaml file
    ros2 run usb_cam usb_cam_node_exe --ros-args --params-file /path/to/colcon_ws/src/usb_cam/config/params.yaml
    ```
    
3. 명령어에 파라미터를 매개변수로 주어 실행 시 ← Tier4의 C1 카메라를 운용 시, 하위와 같은 파라미터를 주어야 합니다.
    
    ```bash
    ros2 run usb_cam usb_cam_node_exe --ros-args \
      -p video_device:=/dev/video0 \ ## 카메라가 video0로 연결되어 있는 경우
      -p framerate:=30.0 \
      -p pixel_format:=uyvy \
      -p image_width:=1920 \
      -p image_height:=1280
    ```
    

**(❗주의 : 운용하는 카메라에 따라 지원하는 포맷, 해상도, 프레임률 등이 다르므로 주의하여 파라미터를 조정해야 합니다.)**

3번에 해당하는 명령어를 실행한 결과, 다음과 같은 출력을 볼 수 있습니다.

```bash
[INFO] [1719487586.064855724] [usb_cam]: camera_name value: default_cam
[WARN] [1719487586.065017808] [usb_cam]: framerate: 30.000000
[INFO] [1719487586.081875735] [usb_cam]: using default calibration URL
[INFO] [1719487586.081912546] [usb_cam]: camera calibration URL: file:///home/haunjo/.ros/camera_info/default_cam.yaml
[ERROR] [1719487586.082027933] [camera_calibration_parsers]: Unable to open camera calibration file [/home/haunjo/.ros/camera_info/default_cam.yaml]
[WARN] [1719487586.082079984] [usb_cam]: Camera calibration file /home/haunjo/.ros/camera_info/default_cam.yaml not found
[INFO] [1719487586.082135745] [usb_cam]: Starting 'default_cam' (/dev/video0) at 1920x1280 via mmap (uyvy) at 30 FPS
[INFO] [1719487586.150519209] [usb_cam]: Capability flag: 0x1000
[INFO] [1719487586.159775631] [usb_cam]: Set framerate to be 30
[INFO] [1719487586.283734071] [usb_cam]: This Cameras Supported Formats:
[INFO] [1719487586.283894575] [usb_cam]:   UYVY 4:2:2[Index: 0, Type: 1, Flags: 0, PixelFormat: 59565955]
[INFO] [1719487586.283943194] [usb_cam]:   width: 1920 x height: 1280
[INFO] [1719487586.283980215] [usb_cam]:   1 1 / 30
[INFO] [1719487586.284012944] [usb_cam]:   1 1 / 20
[INFO] [1719487586.284044655] [usb_cam]:   1 1 / 10
```

### 2개 이상의 `usb_cam_node` 실행하기

```bash
ros2 run usb_cam usb_cam_node_exe --remap __ns:=/usb_cam_0 --params-file /path/to/usb_cam/config/params_0.yaml
ros2 run usb_cam usb_cam_node_exe --remap __ns:=/usb_cam_1 --params-file /path/to/usb_cam/config/params_1.yaml
```

2개 이상의 노드를 실행할 때는 `--remap` 키워드를 사용하여 `namespace` 를 정의해 줍니다.

> *Compressed Image를 가져오는 내용에 대해서 이 문서에서는 다루지 않습니다. https://github.com/ros-drivers/usb_cam 를 참고하세요.*
> 

## Step 2. 이미지 조회

---

`usb_cam_node` 는 카메라로부터 수집한 이미지를 `/image_raw` 라는 이름의 토픽으로 발행합니다. 이 **이미지를 GUI 상에서 조회하기 위해서**는 ROS2의 이미지 조회 패키지인 `rqt_image_view` 를 사용해야 합니다.

### `rqt_image_view`

```bash
ros2 run rqt_image_view rqt_image_view 
```

![rqt_image_view 실행 화면](ROS2%20usb_cam%20node%20%E1%84%80%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%83%E1%85%B3%201ac69d1c156a427dba75ac158165e017/Untitled.png)

rqt_image_view 실행 화면

## Step 3. 파라미터 설정

---

카메라는 `framerate`, `image_width` , `image_height` , `brightness` , `exposure` 등 10개 내외의 파라미터를 통해 센서의 처리가 조정됩니다. `usb_cam` 의 경우 사용자가  `param.yaml` 에 파라미터를 **사용자 정의** 함으로써 노드가 이를 활용하도록 할 수 있습니다.

### `param.yaml`

```yaml
/**:
    ros__parameters:
      video_device: "/dev/video0"
      framerate: 30.0      io_method: "mmap"
      frame_id: "camera"
      pixel_format: "mjpeg2rgb"  # see usb_cam/supported_formats for list of supported formats
      av_device_format: "YUV422P"
      image_width: 640
      image_height: 480
      camera_name: "test_camera"
      camera_info_url: "package://usb_cam/config/camera_info.yaml"
      brightness: -1 # 밝기
      contrast: -1 # 대비
      saturation: -1 # 채도
      sharpness: -1 # 선명도
      gain: -1 # 게인 (낮은 조도 환경에서 이미지를 밝게 하기 위해 사용)
      auto_white_balance: true 
      white_balance: 4000
      autoexposure: true
      exposure: 100 # 노출 (높을수록 더 많은 빛을 받아 이미지가 밝아지나, 움직이는 물체가 흐려질 수 있음)
      autofocus: false
      focus: -1
```

### 내부 파라미터 설정

카메라의 내부 파라미터(Intrinsic Parameters)를 알고 있으면 렌즈의 왜곡을 보정하는데 활용하여 **카메라가 보는 세상과 실제 세상의 차이를 줄일** **수 있습니다**. 이를 위해 카메라의 내부 파라미터를 유도하는 Callibration 과정이 필요하지만, 이는 별도의 문서에서 다루고 본 문서에서는 Callibration을 완료했다는 가정 하에 해당 내용을 안내합니다.

### `Camera_info.yaml`

- `camera_matrix`: 내부 파라미터
- `distortion_model` : 왜곡 보정 모델, plumb_bob 이 대표적
- `distortion_coefficients` : 왜곡 보정 계수
- `rectification_matrix` : 스테레오 카메라에서 다루는 파라미터
- `projection_matrix` : 왜곡 보정이 처리된, 최종 projection할 행렬

```yaml
image_width: 640
image_height: 480
camera_name: test_camera
camera_matrix:
  rows: 3
  cols: 3
  data: [438.783367, 0.000000, 305.593336, 0.000000, 437.302876, 243.738352, 0.000000, 0.000000, 1.000000]
distortion_model: plumb_bob
distortion_coefficients:
  rows: 1
  cols: 5
  data: [-0.361976, 0.110510, 0.001014, 0.000505, 0.000000]
rectification_matrix:
  rows: 3
  cols: 3
  data: [0.999978, 0.002789, -0.006046, -0.002816, 0.999986, -0.004401, 0.006034, 0.004417, 0.999972]
projection_matrix:
  rows: 3
  cols: 4
  data: [393.653800, 0.000000, 322.797939, 0.000000, 0.000000, 393.653800, 241.090902, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000]
```

### 참고자료

---

<aside>
💡 [https://github.com/ros-drivers/usb_cam](https://github.com/ros-drivers/usb_cam) # usb_cam 깃허브
[https://tier4.github.io/edge-auto-docs/user_manual/GMSL2-USB-3.0-conversion-kit-user-manual.html](https://tier4.github.io/edge-auto-docs/user_manual/GMSL2-USB-3.0-conversion-kit-user-manual.html) # tier4 c1 usb-gmsl converter manual

</aside>