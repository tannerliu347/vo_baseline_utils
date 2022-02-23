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
    if os.path.isdir(os.path.join(old_depth_dir, '..', new_depth_dir)):
        return
    os.mkdir(os.path.join(old_depth_dir, '..', new_depth_dir))
    # read from npy and save as 16 bit png depth images
    for npy_dep in os.listdir(old_depth_dir):
        dep = np.load(os.path.join(old_depth_dir, npy_dep))
        img = np.zeros(dep.shape, dtype=np.uint16)
        # for r in range(dep.shape[0]):
        #     for c in range(dep.shape[1]):
        #         new_val = dep[r, c] * 500.0
        #         if new_val > np.iinfo(img.dtype).max:
        #             new_val = 0
        #         img[r, c] = new_val
        img = dep * 2000 # use 500 for outdoor scenes and 2000 for indoor scenes
        img = img.astype(np.uint16)
        img[img > 32500] = 0.0
        # write to new png file
        filename = npy_dep[:-4]
        cv2.imwrite(os.path.join(old_depth_dir, '..', new_depth_dir, filename + '.png'), img)

def save_calibration_txt(save_dir):
    f = open(os.path.join(save_dir, 'calibration.txt'), 'w')
    f.write('320.0 320.0 320.0 240.0')
    f.close()


def read_file_list(filename):
    """
    Reads a trajectory from a text file. 
    
    File format:
    The file format is "stamp d1 d2 d3 ...", where stamp denotes the time stamp (to be matched)
    and "d1 d2 d3.." is arbitary data (e.g., a 3D position and 3D orientation) associated to this timestamp. 
    
    Input:
    filename -- File name
    
    Output:
    dict -- dictionary of (stamp,data) tuples
    
    """
    file = open(filename)
    data = file.read()
    lines = data.replace(","," ").replace("\t"," ").split("\n") 
    list = [[v.strip() for v in line.split(" ") if v.strip()!=""] for line in lines if len(line)>0 and line[0]!="#"]
    list = [(float(l[0]),l[1:]) for l in list if len(l)>1]
    return dict(list)

def associate(first_list, second_list,offset,max_difference):
    """
    Associate two dictionaries of (stamp,data). As the time stamps never match exactly, we aim 
    to find the closest match for every input tuple.
    
    Input:
    first_list -- first dictionary of (stamp,data) tuples
    second_list -- second dictionary of (stamp,data) tuples
    offset -- time offset between both dictionaries (e.g., to model the delay between the sensors)
    max_difference -- search radius for candidate generation

    Output:
    matches -- list of matched tuples ((stamp1,data1),(stamp2,data2))
    
    """
    # first_keys = first_list.keys()
    # second_keys = second_list.keys()
    first_keys = list(first_list)
    second_keys = list(second_list)
    potential_matches = [(abs(a - (b + offset)), a, b) 
                         for a in first_keys 
                         for b in second_keys 
                         if abs(a - (b + offset)) < max_difference]
    potential_matches.sort()
    matches = []
    for diff, a, b in potential_matches:
        if a in first_keys and b in second_keys:
            first_keys.remove(a)
            second_keys.remove(b)
            matches.append((a, b))
    
    matches.sort()
    return matches

def save_associate_txt(dir):
    first_list = read_file_list(os.path.join(dir, 'rgb.txt'))
    second_list = read_file_list(os.path.join(dir, 'depth.txt'))

    matches = associate(first_list, second_list,float(0),float(0.02))    

    f = open(os.path.join(dir, 'associated.txt'), 'w')

    # if args.first_only:
    #     for a,b in matches:
    #         print("%f %s"%(a," ".join(first_list[a])))
    # else:
    for a,b in matches:
        # print("%f %s %f %s"%(a," ".join(first_list[a]),b-float(args.offset)," ".join(second_list[b])))
        f.write("%f %s %f %s\n"%(a," ".join(first_list[a]),b-float(0)," ".join(second_list[b])))

    f.close()


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
    # generate calibration
    save_calibration_txt(dir)
    # generate association file
    save_associate_txt(dir)
