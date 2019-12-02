# coding: utf8
import sys, os, inspect
import numpy as np
import pandas as pd
import argparse
import importlib

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
maindir = os.path.dirname(parentdir)

resampling_spec = importlib.util.spec_from_file_location("resampling", "%s/src/resampling.py"%maindir)
resampling = importlib.util.module_from_spec(resampling_spec)
resampling_spec.loader.exec_module(resampling)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("video", help = "the path of the video to process.")
    parser.add_argument("out_dir", help = "the path where to store the results.")
    parser.add_argument("--demo",'-d', help = "If this script is using for demo.", action = "store_true")
    parser.add_argument("--eyetracking",'-eye', help = "the path of the eyetracking file (for demo).")
    parser.add_argument("--facial_features",'-faf', help = "the path of the facial features file (csv file) (for demo).")
    args = parser.parse_args()

    if args. out_dir == 'None':
        usage ()
        exit ()

    # Input directory and Output file
    subject = args. video.split ('/')[-2]
    conversation_name = args. video.split ('/')[-1]. split ('.')[0]
    out_file = args. out_dir + conversation_name

    if args. demo:
    	eye_tracking_file = args. eyetracking
    	openface_file = args. facial_features
    else:
    	eye_tracking_file = "time_series/%s/gaze_coordinates_ts/%s.pkl"%(subject, conversation_name)
    	openface_file = "time_series/%s/facial_features_ts/%s/%s.csv"%(subject, conversation_name, conversation_name)

    if os.path.exists (out_file + '.pkl'):
        print ("Warning, file already processed")
        exit (1)

    if not os.path.exists (openface_file):
        print ("Error, file %s does not exists"%openface_file)
        exit (1)

    """ 1/30: image frequency of videos, equivalent to 1799 images per minute """
    video_index = [1.0 / 30.0 ]
    for i in range (1, 1799):
        video_index. append (1.0 / 30.0 + video_index [i - 1])

    """ compute the index of the index BOLD signal frequency """
    physio_index = [0.6]
    for i in range (1, 50):
    	physio_index. append (1.205 + physio_index [i - 1])

    eye_tracking_data = pd. read_pickle (eye_tracking_file)
    eye_tracking_data = eye_tracking_data . loc [:, ["Time (s)", "x", "y"]]. values. astype (float)
    openface_data = pd. read_csv (openface_file, sep = ',', header = 0)

    contractions = pd.DataFrame ()
    contractions ["Time (s)"] = openface_data [" timestamp"]. values
    contractions ["mouth_cont"] = openface_data. loc [:,[" AU10_r", " AU12_r"," AU14_r"," AU15_r"," AU17_r"," AU20_r", " AU23_r", " AU25_r", " AU26_r"]]. sum (axis = 1)

    contractions["eyes_cont"] = openface_data. loc [:, [" AU01_r", " AU02_r", " AU04_r", " AU05_r", " AU06_r", " AU07_r", " AU09_r"]]. sum (axis = 1)

    """ resampling """
    output_time_series = pd.DataFrame (resampling. resample_ts (contractions. values, physio_index, mode = "mean"), columns = contractions.columns)
    output_time_series.to_pickle (out_file + ".pkl")

    '''coordinates_resampled = resampling. resample_ts (eye_tracking_data, video_index, mode = "mean")
    print (coordinates_resampled. shape)

    E_eyet = np. sum (np. square (np. diff (coordinates_resampled[:,1:], axis = 0)), axis = 0)
    print (E_eyet. shape)'''
