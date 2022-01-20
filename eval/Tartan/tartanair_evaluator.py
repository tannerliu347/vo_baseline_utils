# Modified by Tianyi Liu

# Copyright (c) 2020 Carnegie Mellon University, Wenshan Wang <wenshanw@andrew.cmu.edu>
# For License information please see the LICENSE file in the root directory.

import numpy as np
from evaluator_base import ATEEvaluator, RPEEvaluator, KittiEvaluator, transform_trajs, quats2SEs
from os.path import isdir, isfile
from scipy.spatial.transform import Rotation as R
import argparse

# from trajectory_transform import timestamp_associate

class TartanAirEvaluator:
    def __init__(self, scale = False, round=1):
        self.ate_eval = ATEEvaluator()
        self.rpe_eval = RPEEvaluator()
        self.kitti_eval = KittiEvaluator()

    def convert_pose_frame(self, est_traj):
        res = np.zeros_like(est_traj)
        # define the transform Tartan cam to our cam
        rot_x_n90 = np.array([[1.0,  0.0, 0.0],
                              [0.0,  0.0, 1.0],
                              [0.0, -1.0, 0.0]])
        rot_z_n90 = np.array([[ 0.0, 1.0, 0.0],
                              [-1.0, 0.0, 0.0],
                              [ 0.0, 0.0, 1.0]])
        T_tar_our = np.eye(4)
        T_tar_our[:3, :3] = rot_x_n90 @ rot_z_n90
        for i in range(est_traj.shape[0]):
            x, y, z = est_traj[i, 0:3]
            qx, qy, qz, qw = est_traj[i, 3:]
            r = R.from_quat([qx, qy, qz, qw])
            T_our_wld = np.eye(4)
            T_our_wld[:3, :3] = r.as_matrix()
            T_our_wld[:3, 3] = np.array([x, y, z])
            T_tar_wld = T_our_wld @ T_tar_our
            new_r = R.from_matrix(T_tar_wld[:3, :3])
            res[i, 0:3] = T_tar_wld[:3, 3]
            res[i, 3:] = new_r.as_quat()
        return res
        
    def evaluate_one_trajectory(self, gt_traj_name, est_traj_name, scale=False):
        """
        scale = True: calculate a global scale
        """
        # load trajectories
        gt_traj = np.loadtxt(gt_traj_name)
        est_traj = np.loadtxt(est_traj_name)

        # convert our camera frame to Tartan Air's NED frame
        # est_traj = self.convert_pose_frame(est_traj)

        if gt_traj.shape[0] != est_traj.shape[0]:
            raise Exception("POSEFILE_LENGTH_ILLEGAL")
        if gt_traj.shape[1] != 7 or est_traj.shape[1] != 7:
            raise Exception("POSEFILE_FORMAT_ILLEGAL")

        # transform and scale
        gt_traj_trans, est_traj_trans, s = transform_trajs(gt_traj, est_traj, scale)
        gt_SEs, est_SEs = quats2SEs(gt_traj_trans, est_traj_trans)

        ate_score, gt_ate_aligned, est_ate_aligned = self.ate_eval.evaluate(gt_traj, est_traj, scale)
        rpe_score = self.rpe_eval.evaluate(gt_SEs, est_SEs)
        kitti_score = self.kitti_eval.evaluate(gt_SEs, est_SEs)

        return {'ate_score': ate_score, 
                'rpe_score': rpe_score, 
                'kitti_score': kitti_score}

if __name__ == "__main__":
    # parse optional arguments
    parser = argparse.ArgumentParser(description='Needs groundtruth_traj and evaluate_traj directory.')
    parser.add_argument('gt_traj', metavar='gt', nargs='+',
                        help='path to groundtruth trajectory txt file')
    parser.add_argument('ev_traj', metavar='eval', nargs='+',
                    help='path to groundtruth trajectory txt file')

    args = parser.parse_args()
    # scale = True for monocular track, scale = False for stereo track
    aicrowd_evaluator = TartanAirEvaluator()
    result = aicrowd_evaluator.evaluate_one_trajectory(args.gt_traj[0], args.ev_traj[0], scale=True)
    # result = aicrowd_evaluator.evaluate_one_trajectory('pose_gt.txt', 'pose_est.txt', scale=True)
    print(result)
