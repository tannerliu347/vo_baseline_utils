# Prepare Tartan Air to be used on BAD-SLAM
# save npy depth as png
# generates text file of all image filenames (tum format)

import os
import argparse
import numpy as np
import cv2

def gen_full_list(parent_dir, sub_dir, filename):
    rgb_dir = os.path.join(parent_dir, sub_dir)
    txt_dir = os.path.join(parent_dir, filename)
    f = open(txt_dir, "w")
    for file in sorted(os.listdir(rgb_dir)):
        timestamp = file[:6]
        rel_path = os.path.join(sub_dir, file)
        f.write('{}  {}\n'.format(timestamp, rel_path))
    f.close()

def save_png_depth(old_depth_dir, new_depth_dir):
    # read from npy and save as 16 bit png depth images
    for npy_dep in os.listdir(old_depth_dir):
        dep = np.load(os.path.join(old_depth_dir, npy_dep))
        img = np.zeros(dep.shape, dtype=np.uint16)
        for r in range(dep.shape[0]):
            for c in range(dep.shape[1]):
                new_val = dep[r, c] * 5000.0
                if new_val > np.iinfo(img.dtype).max:
                    new_val = 0
                img[r, c] = new_val
        # write to new png file
        filename = npy_dep[:-4]
        cv2.imwrite(os.path.join(old_depth_dir, '..', new_depth_dir, filename + '.png'), img)


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='Needs a tartan air trajectory directory. \
                                                  e.g. python3 segment_classes.py /home/USER/TartanAir/abandonedfactory/Easy/P001/')
    parser.add_argument('trj_dir', metavar='trj_dir', nargs='+',
                        help='path to tartan air trajectory folder')
    args = parser.parse_args()
    dir = args.trj_dir[0]

    # save as png
    save_png_depth(dir + 'depth_left', 'depth_left_png')
    # generate rgb.txt that contains path to all rgb images
    gen_full_list(dir, 'image_left', 'rgb.txt')
    # same for depth
    gen_full_list(dir, 'depth_left_png', 'depth.txt')

