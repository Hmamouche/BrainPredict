"""
    Author: Youssef Hmamouche
    Year: 2019
    Compute predictions of time series (already extracted from raw data) based on pretrained models
"""

import os
import glob
import pandas as pd
import numpy as np
import joblib
import argparse
from ast import literal_eval
import sys
from tqdm import tqdm

from sklearn.metrics import recall_score, precision_score, f1_score, average_precision_score


#---------------------------------------------------#
def reorganize_data (data_, lag, step = 1):
	"""
	    step: ratio between frequencies compared to bold signal time-step, which is 1.205 s.
	    lag: lag parameter
	"""
	out_data = []
	real_lag = lag - 2

	for i in range (lag, len (data_), step):
		row = []
		for j in range (data_. shape [1]):
			row = row + list (data_ [i - lag : i -  lag + real_lag, j]. flatten ())
		out_data. append (row)

	return np. array (out_data)


#---------------------------------------------------#
def get_features_from_lagged (lagged_variables):
	features = set (['_'. join (a.split ('_')[0:-1]) for a in lagged_variables])
	return ','. join (map (str, list (features)))

#---------------------------------------------------#
def get_predictors_dict (model_name, region, type, path):
    """
    model_name: name the prediction model
    region: brain area
    type: interaction type (h (human-human) or r (human-robot))
    """
    model_params = pd. read_csv ("%s/results/prediction/%s_H%s.tsv"%(path, model_name, type. upper ()), sep = '\t', header = 0)
    predictors = model_params . loc [model_params["region"] == "%s"%region]["selected_predictors"]. iloc [0]
    reduced_predictors = model_params . loc [model_params["region"] == "%s"%region]["predictors_dict"]. iloc [0]

    return literal_eval (predictors), literal_eval (reduced_predictors)

#---------------------------------------------------#
if __name__ == '__main__':
    parser = argparse. ArgumentParser ()
    requiredNamed = parser.add_argument_group('Required arguments')
    requiredNamed. add_argument ('--regions','-rg', help = "Numbers of brain areas to predict (see brain_areas.tsv)", nargs = '+', type=int)
    requiredNamed. add_argument ('--type','-t', help = ' conversation type (human or robot)')
    requiredNamed. add_argument ('--lag','-lag', default = 6, type=int)
    requiredNamed. add_argument ('--pred_module_path','-pmp', help = "path of the prediction module")
    requiredNamed. add_argument ('--input_dir','-in', help = "path of input directory")

    args = parser.parse_args()

    """ load the best models for each regions """
    if args. type == 'h':
    	conversation_type = 'HH'
    elif args. type == 'r':
    	conversation_type = 'HR'
    else:
    	print ("Error in arguments, type of conversation missing, use -h for help!")
    	exit (1)

    if args. pred_module_path [-1] == '/':
    	args. pred_module_path = args. pred_module_path [:-1]

    out_dir =  "%s/Outputs/generated_time_series/"%args.input_dir

    # read brain areas codes
    regions = []
    brain_areas_desc = pd. read_csv ("brain_areas.tsv", sep = '\t', header = 0)
    for num_region in args. regions:
    	regions. append (brain_areas_desc . loc [brain_areas_desc ["Code"] == num_region, "Name"]. values [0])

    # Read the computed multomodal time series
    all_data = pd. read_csv ("%s/Outputs/generated_time_series/features.csv"%args.input_dir, sep = ';', header = 0)

    # time index
    time_index = all_data. iloc [:, 0]. values

    # Keep just features (remove time column)
    all_data = all_data. iloc [:, 1:]
    columns = all_data. columns

    # get names of lagged variables of transform the data to a temporal representation depending on the lag parameter
    lagged_names = []
    for col in columns:
    	lagged_names. extend ([col + "_t%d"%(p) for p in range (args. lag, 2, -1)])

    all_data = pd. DataFrame (reorganize_data (all_data. values, args. lag), columns = lagged_names)


    # Load trained models found as best for each brain area in the training step
    trained_models = glob. glob ("%s/trained_models/*%s.pkl"%(args.pred_module_path,conversation_type))

    # dictionary of predictions: results
    preds = {}
    predictors_variables = {}

    # Predict each brain area
    for region in tqdm (regions):
        print (region)
        predictors_data = pd. DataFrame ()
        predictors_data. columns = []
        fname = ""
        for filename in trained_models:
        	if region in  filename:
        		fname = filename
        		break

        model_name = fname. split ('/')[-1]. split ('_') [0]

        model = joblib. load (fname)

        # get predictors from the training results
        predictors, reduced_predictors = get_predictors_dict (model_name, region, args. type, args.pred_module_path)

        # Select data of the selected features
        predictors_data = all_data. loc [:, predictors]

        # Make predictions
        pred = model. predict (predictors_data)

        # Store the predictions of each region in the dictionary
        preds [region] = [0 for i in range (args. lag)] + pred. tolist ()

        # Selected variables without lags
        #predictors_variables [region] = get_features_from_lagged (predictors)
        predictors_variables [region] = reduced_predictors


    # Store the predictions
    preds_var = pd.DataFrame ()
    for col in predictors_variables. keys ():
    	preds_var[col] = [str (predictors_variables [col])]

    # Store the predictions
    pd. DataFrame (preds, index = time_index). to_csv ("%s/Outputs/predictions.csv"%args.input_dir, sep = ';', index_label = ["Time (s)"])
    preds_var. to_csv ("%s/Outputs/predictors.csv"%args.input_dir, sep = ';', index = False)
