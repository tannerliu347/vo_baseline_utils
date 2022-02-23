import csv
import os
import argparse

# parse arguments
parser = argparse.ArgumentParser(description='Needs a TUM format trajectory file. \
                                                e.g. python3 tum_traj_to_tartan.py /home/USER/results/traj.txt')
parser.add_argument('trj_dir', metavar='trj_dir', nargs='+',
                    help='path to trajectory txt file')
args = parser.parse_args()

input_file = args.trj_dir[0]

with open(input_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\n')
    next(csv_reader) # skip line 0
    # trim new traj file name
    old_name = input_file[:input_file.find('.txt')]
    output_file = open(old_name + "_tartan.txt", 'w')
    for row in csv_reader:
        start_idx = row[0].find(' ')
        # print(row[0][start_idx + 1:])
        output_file.write(row[0][start_idx + 1:] + '\n')

output_file.close()
os.remove(input_file)