# Iterate through a directory of Tartan Air dataset segmentation npy files
# Find total number of classes
# Generate remapping of class numbers from 0 - total number of classes

from asyncore import write
from enum import unique
import numpy as np
import cv2
import os
import argparse

def get_airsim_classes(directory, visual=False):
    """Returns a dictionary with airsim class as key, pixel occurance as value, sorted
    """
    class_count = dict()
    for file in sorted(os.listdir(directory)):
        filename = os.fsencode(file)
        abs_path = os.path.join(directory, filename)
        seg = np.load(abs_path)
        uniques, counts = np.unique(seg, return_counts=True)
        for uni, cnt in zip(uniques, counts):
            if uni not in class_count:
                class_count[uni] = 0
            class_count[uni] = class_count[uni] + cnt
        if visual:
            cv2.imshow("haha", seg)
            cv2.waitKey(5)
    class_count = {k: v for k, v in sorted(class_count.items(), key=lambda item: -item[1])}
    return class_count

def merge_k_classes(class_count, k=10):
    new_mapping = dict()
    for key, value in class_count.items():
        if len(new_mapping) > 8:
            new_mapping[key] = 9
        else:
            new_mapping[key] = len(new_mapping)
    return new_mapping

def write_new_mapping(directory, mapping):
    # write new mapping to a file
    write_path = os.path.join(directory, os.fsencode('../seg_map.txt'))
    f = open(write_path, "w")
    for key, value in mapping.items():
        f.write('{} : {}\n'.format(key, value))
    f.close()

if __name__ == '__main__':
    # parse optional arguments
    parser = argparse.ArgumentParser(description='Needs a tartan air segmentation data directory. \
                                                  e.g. python3 segment_classes.py /home/USER/TartanAir/abandonedfactory/Easy/P001/seg_left/')
    parser.add_argument('seg_dir', metavar='seg_dir', nargs='+',
                        help='path to tartan air segmentation folder')
    args = parser.parse_args()
    dir = args.seg_dir[0]
    old_classes = get_airsim_classes(os.fsencode(dir))
    print('Number of segmentation classes: {}'.format(len(old_classes)))
    new_mapping = merge_k_classes(old_classes)
    write_new_mapping(os.fsencode(dir), new_mapping)