# Arrival_project
![](./assets/poster.png)

## Dataset
### [자율주행 - 버스 승객 승하차 영상](https://aihub.or.kr/aidata/34166) : Camera C (General C)
- Removed List
```
...\ele\[ele]attend_270C
...\etc\[etc]attend_154C
...\hospital\[hospital]attend_392C
...\hospital\[hospital]leave_251C
```
- Target(demonstration result)

```
reselecting

type 1
[hospital]attend_067C

type 2
[mid_high]leave_354C

```
![](./assets/check_frame.png)

![](./assets/people_in_one_scene_train.png)
![](./assets/people_in_one_scene_valid.png)
![](./assets/people_in_one_frame_train.png)
![](./assets/people_in_one_frame_valid.png)

## Modeling
- 하차 전 약 35프레임에서의 각 사람의 skeleton data를 time series data로 만들어서 하차할 것인지 하차하지 않을 것인지 Intention Prediction

## TODO
- [ ] 데이터 분석
    - [x] 결점 데이터 제거
    - [ ] get off가 True vs. False인 사람 비율
    - [ ] 한 frame 당/ scene 당 나타나는 사람 수 비율
- [ ] 데이터셋 클래스
- [ ] 간단한 lstm 모델
- [ ] 시각화
- [ ] TF multi pose 모델이랑 연결

## Repo에 있는 코드 설명
- `check_people.py`:
- `find_getoff.py`:
- `cutoff_box.py`:
- `simple_dataset.py`: 각 사람(id)별 키포인트 시계열 데이터로 가져오기
- `train.py`: simple lstm model로 training
- `inference.py`: 
- `generate_video.py`:
- `tf2_multipose.py`:

## Reference
- [Scale invariant angle label](https://matplotlib.org/stable/gallery/text_labels_and_annotations/angle_annotation.html#sphx-glr-gallery-text-labels-and-annotations-angle-annotation-py)
- [seaborn.histplot](https://seaborn.pydata.org/generated/seaborn.histplot.html)

### Baseline
- [Unified Framework for Pedestrian Detection & Intention Classification](https://github.com/mjpramirez/Volvo-DataX)
- [FuSSI-Net: Fusion of Spatio-temporal Skeletons for Intention Prediction Network](https://matthew29tang.github.io/pid-model/#/)

### OD+Tracking
- [Yolov5 + Deep Sort with PyTorch](https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch)
    - `python track.py --source [village]day_001B.mp4 --yolo_weights yolov5/weights/crowdhuman_yolov5m.pt --classes 0 --save-txt --save-vid`
    - `frame_idx, id, bbox_left, bbox_top, bbox_w, bbox_h, -1, -1, -1, -1)`
- [YOLOv4-Cloud-Tutorial](https://github.com/theAIGuysCode/YOLOv4-Cloud-Tutorial)

### Pose Estimation
- [Deep High-Resolution Representation Learning for Human Pose Estimation (CVPR 2019)](https://github.com/leoxiaobin/deep-high-resolution-net.pytorch)
- [Multi Person PoseEstimation By PyTorch](https://github.com/tensorboy/pytorch_Realtime_Multi-Person_Pose_Estimation)
    - `python Demo_video.py -backbone {CMU or Mobilenet} -video {video path} -scale {scale to image} -show {}`