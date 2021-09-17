# Utils for evaluating VO systems
Util functions to evaluate performance on ORB-SLAM2, Stereo-DSO

## Current evaluation approach:

### ORB-SLAM2 + KITTI:
1. Run ORB-SLAM2/Examples/Stereo/stereo_kitti.cc to generate result trajectory(in KITTI format)
2. Use KITTI official evaluate_odometry_kitti.cpp : evaluate_odometry_kitti sequence_num gt_directory gt_file result_dir result_file
```
eval/KITTI/evaluate_odometry_kitti 00 groundTruth 00.txt results resultTraj.txt
```
This outputs traslation error (%) and rotation error (deg/m)

### ORB-SLAM2 + EuRoc:
1. Run ORB-SLAM2/Examples/Stereo/stereo_euroc.cc to generate result trajectory(in TUM format)
2. Use evaluate_ate_scale.py
```
eval/EuRoc/eval_EuRoc/evaluate_ate_scale.py --verbose gt_dir/data.csv result.txt
```
This outputs ATE

### Stereo-DSO + KITTI:
1. Use calibration files from run/KITTI/stereo-dso/KITTI_calib
2. Run sdso to generate result trajectory(in KITTI format):
```
build/bin/dso_dataset files=KITTI_dataset_dir/sequences/XX calib=calib_file_dir preset=0 mode=1 outputfile=XX.txt
```
3. Use KITTI official evaluate_odometry_kitti.cpp

### Stereo-DSO + EuRoc:
1. Use calibration files from XXXXXXXXXX
2. Run sdso to generate result trajectory(int KITTI format)
3. Obtain result trajectory timestamps using convert/generate_timestamps.cpp, passing result trajectory from ORB_SLAM:
```
convert/generate_timestamps TUM_format_traj output_file
```
4. Use convert/kitti_2_tum.py to convert timestamp + KITTI_traj to TUM format trajectory
5. Use eval_EuRoc/evaluate_ate_scale.py

## Quick note on different trajectory representations
TUM: timestamp + xyz + quaternion

KITTI: flattened SE(3) pose matrix without bottom 0 0 0 1 row

EuRoc: csv with state information in IMU frame