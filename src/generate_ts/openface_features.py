# coding: utf8
import sys, os, inspect
import numpy as np
import pandas as pd
import argparse

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
maindir = os.path.dirname(parentdir)

sys.path.insert (0, maindir)
import src.resampling as resampling

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#===================================================


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("video", help="the path of the video to process.")
	parser.add_argument("out_dir", help="the path where to store the results.")
	parser.add_argument("--show",'-s', help="Showing the video.", action="store_true")
	parser.add_argument("--openface",'-op', help="Showing the video.", default="../../OpenFace")

	args = parser.parse_args()


	if args. out_dir[-1] != '/':
		args. out_dir += '/'

	if args. openface [-1] != '/':
		args. openface += '/'

	# Input directory
	conversation_name = args. video.split ('/')[-1]. split ('.')[0]
	out_file = args. out_dir + conversation_name

	# verify if the file already exists
	if os.path.isfile ("%s.pkl"%out_file):
		print ("Already processed")
		exit (1)
	# Run OpenFace binary program to the video and the given output directory
	os. system (args. openface + "build/bin/FeatureExtraction -q -f %s -out_dir %s" %(args. video, out_file))

	# read csv file
	openface_data = pd. read_csv ("%s/%s.csv"%(out_file, conversation_name), sep=',', header=0)

	# Keeping just  some features : gaze, head pose, and facial unit actions
	movements_cols = [" timestamp", " success", " gaze_angle_x", " gaze_angle_y", " pose_Tx", " pose_Ty", " pose_Tz", " pose_Rx", " pose_Ry", " pose_Rz"]
	action_units_cols = [" AU01_r"," AU02_r"," AU04_r"," AU05_r"," AU06_r"," AU07_r"," AU09_r"," AU10_r"," AU12_r"," AU14_r"," AU15_r"," AU17_r"," AU20_r"," AU23_r", " AU25_r", " AU26_r", " AU45_r"]
	action_units_existence_cols = [" AU01_c"," AU02_c"," AU04_c"," AU05_c"," AU06_c"," AU07_c"," AU09_c"," AU10_c"," AU12_c"," AU14_c"," AU15_c"," AU17_c"," AU20_c"," AU23_c", " AU25_c", " AU26_c", " AU45_c"]
	land_marks_cols = [" x_%d"%i for i in range (68)] + [" y_%d"%i for i in range (68)]


	# Extract only some features from openface results
	data = openface_data. loc [:, movements_cols + action_units_cols + action_units_existence_cols + land_marks_cols]
	data.to_pickle ("%s.pkl"%out_file)

	# remove openface detailed outputs
	os. system ("rm -rf %s"%(out_file))
