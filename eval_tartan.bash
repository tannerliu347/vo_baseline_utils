gt_folder=/home/tannerliu/media/Samsung_T5/tartanair
traj_folder=/home/tannerliu/stereo-dso
difficulty=Hard

for scene in seasonsforest_winter #ocean seasidetown endofworld gascola soulcity
do
echo "evaluating $scene"
python3 eval/Tartan/tartanair_evaluator.py $gt_folder/$scene/$difficulty/P010/pose_left_328.txt $traj_folder/${scene}_${difficulty}.txt
done