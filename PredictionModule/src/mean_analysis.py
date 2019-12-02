import os
import glob
import pandas as pd
import numpy as np
import argparse

from sklearn import preprocessing
from mat4py import loadmat
from sklearn.linear_model import Ridge, Lasso
from sklearn.neural_network import MLPRegressor
from sklearn.decomposition import PCA, IncrementalPCA, KernelPCA

#=============================================
# generate time series from transcriptions files
def process_transcriptions (subject, type = "speech_ts"):
    files = glob. glob ("time_series/%s/%s/*.pkl"%(subject, type))
    return sorted (files)

#===============================================
def generate_stats (subject, type):
    files = process_transcriptions (subject, type)

    HH_data = []
    HR_data = []

    for filename in files:
        data = pd. read_pickle (filename)

        if data. shape [0] < 50:
            print ("Subject: %s, the conversation %s have less than 50 lines"%(subject, filename))
        if "CONV1" in filename:
            HH_data. append (data. mean (axis = 0). tolist ())
        if "CONV2" in filename:
            HR_data. append (data. mean (axis = 0). tolist ())


    HH_data = pd.DataFrame (HH_data, columns = data. columns)
    HR_data = pd.DataFrame (HR_data, columns = data. columns)

    return HH_data, HR_data


#=============================================
if __name__ == '__main__':

    parser = argparse. ArgumentParser ()

    parser. add_argument ("--data_type", "-t", help = "behavioral data type")
    args = parser.parse_args()

    if not os. path. exists ("stats_ts"):
    	os. makedirs ("stats_ts")

    #=======================================================
    #   define the subjects to process: the participants
    #=======================================================
    subjects = ["sub-%02d"%i for i in range (1, 25)]
    for sub in ["sub-01",  "sub-12", "sub-19", "sub-14", "sub-04",  "sub-16"]:
        if sub in subjects:
            subjects. remove (sub)

    hh_data = pd. DataFrame ()
    hr_data = pd. DataFrame ()

    for subject in subjects:
        #print (subject)
        subj_hh, subj_hr = generate_stats (subject,args. data_type)
        hh_data = hh_data. append (subj_hh, ignore_index = True)
        hr_data = hr_data. append (subj_hr, ignore_index = True)

    #print (hh_data)
    hh_data. iloc[:, 1:]. to_csv ("stats_ts/%s_HH.csv"%args. data_type, sep = ';', index = False)
    hr_data. iloc[:, 1:]. to_csv ("stats_ts/%s_HR.csv"%args. data_type, sep = ';', index = False)
