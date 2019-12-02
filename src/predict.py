import os
import glob
import pandas as pd
import numpy as np
import joblib
import argparse
from ast import literal_eval
import sys

from sklearn.metrics import recall_score, precision_score, f1_score, average_precision_score

class toSuppervisedData:
	targets = np.empty([0,0],dtype=float)
	data = np.empty([0,0],dtype=float)

	## constructor
	def __init__(self, X, p, test_data = False, add_target = False):

		self.targets = self.targets_decomposition (X,p)
		self.data = self.matrix_decomposition (X,p, test_data)

		if not add_target:
			self.data = np. delete (self.data, range (0, p), axis = 1)

		delet = []

		if X.shape[1] > 1 and p > 4:
			for j in range (0, self.data. shape [1], p):
				delet. extend ([j + p - i for i in range (1, 3)])

		self.data = np. delete (self.data, delet, axis = 1)

	## p-decomposition of a vector
	def vector_decomposition (self, x, p, test = False):
		n = len(x)
		if test:
			add_target_to_data = 1
		else:
			add_target_to_data = 0

		output = np.empty([n-p,p],dtype=float)

		for i in range (n-p):
			for j in range (p):
				output[i,j] = x[i + j + add_target_to_data]
		return output

	# p-decomposition of a target
	def target_decomposition (self,x,p):
		n = len(x)
		output = np.empty([n-p,1],dtype=float)
		for i in range (n-p):
			output[i] = x[i+p]
		return output

	# p-decomposition of a matrix
	def matrix_decomposition (self,x,p, test=False):
		output = np.empty([0,0],dtype=float)
		out = np.empty([0,0],dtype=float)

		for i in range(x.shape[1]):
			out = self.vector_decomposition(x[:,i],p, test)
			if output.size == 0:
				output = out
			else:
				output = np.concatenate ((output,out),axis=1)

		return output
	# extract all the targets decomposed
	def targets_decomposition (self,x,p):
		output = np.empty([0,0],dtype=float)
		out = np.empty([0,0],dtype=float)
		for i in range(x.shape[1]):
			out = self.target_decomposition(x[:,i],p)
			if output.size == 0:
				output = out
			else:
				output = np.concatenate ((output,out),axis=1)
		return output

#---------------------------------------------------#
def get_predictors (model_name, region, type, path):
    """
    model_name: name the prediction model
    region: brain area
    type: interaction type (h (human-human) or r (human-robot))
    """
    model_params = pd. read_csv ("%s/results/prediction/%s_H%s.tsv"%(path, model_name, type. upper ()), sep = '\t', header = 0)
    predictors = model_params . loc [model_params["region"] == "%s"%region]["predictors_dict"]. iloc [0]

    return predictors

#---------------------------------------------------#
def get_predictors_dict (model_name, region, type, path):
    """
    model_name: name the prediction model
    region: brain area
    type: interaction type (h (human-human) or r (human-robot))
    """
    model_params = pd. read_csv ("%s/results/prediction/%s_H%s.tsv"%(path, model_name, type. upper ()), sep = '\t', header = 0)
    predictors = model_params . loc [model_params["region"] == "%s"%region]["selected_predictors"]. iloc [0]

    return predictors

#---------------------------------------------------#
def speech_features (pred_path, compute_features, out_dir):
    """
    generate speech features from audio files
    pred_path: path of the prediction module
    compute_features: logical, for computing the features or not (if they alreadu exists)
    out_dir: output directory
    """

    #print ("Processing speech")
    if compute_features:
    	audio_path = "Inputs/speech"
    	'''os. system ("python %s/src/utils/SPPAS/sppas/bin/normalize.py -r %s/src/utils/SPPAS/resources/vocab/eng.vocab -I %s  -l fra -e .TextGrid --quiet"%(pred_path, pred_path, audio_path))
    	os. system ("python %s/src/utils/SPPAS/sppas/bin/phonetize.py  -I %s -l fra -e .TextGrid"%(pred_path, audio_path))
    	os. system ("python %s/src/utils/SPPAS/sppas/bin/alignment.py  -I %s -l fra -e .TextGrid --aligner basic"%(pred_path, audio_path))'''
    	#os. system ("python %s/src/generate_ts/speech_features.py Inputs/speech/ %s/"%(pred_path,out_dir))
    	out = os. system ("python %s/src/generate_ts/speech_features.py Inputs/speech/ %s/ -l"%(pred_path,out_dir))

    if out_dir[-1] != '/':
    	out_dir += '/'
    speech = pd. read_pickle (out_dir + "speech_features.pkl")
    speech_left = pd. read_pickle (out_dir + "speech_features_left.pkl")
    return speech_left, speech

#---------------------------------------------------#
def facial_features (pred_path, compute_features, out_dir, openface_path):
    """ facial features  """

    #print ("Processing video")
    video_path = glob.glob ("Inputs/video/*.avi")[0]

    if out_dir[-1] != '/':
    	out_dir += '/'

    if compute_features:
    	out = os. system ("python %s/src/generate_ts/facial_action_units.py %s %s -op %s"%(pred_path, video_path, out_dir, openface_path))

    video_features = glob.glob (out_dir + "*.pkl")[0]
    video_feats = pd. read_pickle (video_features)
    return video_feats

#---------------------------------------------------#
def eyetracking_features (pred_path, compute_features, out_dir):
    """ eyetracking data """

    #print ("Processing eyetracking data")
    if out_dir[-1] != '/':
    	out_dir += '/'

    if compute_features:
    	video_path = glob.glob ("Inputs/video/*.avi")[0]
    	openface_features = glob.glob ("Outputs/generated_time_series/video/"+ video_path[:-4]. split ('/')[-1] + "/*.csv")[0]
    	gaze_coordinates_file = glob.glob ("Inputs/eyetracking/*.pkl")[0]

    	out = os. system ("python %s/src/generate_ts/eyetracking.py %s %s -d -eye %s -faf %s -sv"%(pred_path, video_path, out_dir, gaze_coordinates_file, openface_features))

    eyetracking_filename = glob.glob ("Outputs/generated_time_series/eyetracking/*.pkl")[0]
    eyetracking = pd. read_pickle (eyetracking_filename)

    return eyetracking

#---------------------------------------------------#
if __name__ == '__main__':
	parser = argparse. ArgumentParser ()
	parser. add_argument ('--regions','-rg', nargs = '+', type=int)
	parser. add_argument ('--type','-t', help = ' conversation type (human or robot)')
	parser. add_argument ('--lag','-lag', default = 6, type=int)
	parser. add_argument ('--openface_path','-ofp', help = "path of Openface")
	parser. add_argument ('--pred_module_path','-pmp', help = "path of the prediction module")
	parser. add_argument ("--generate", "-g", help = "generate features from input signals", action="store_true")
	parser. add_argument ("--predict", "-p", help = "make predictions", action="store_true")
	args = parser.parse_args()


	if args. pred_module_path [-1] == '/':
	    args. pred_module_path = args. pred_module_path [:-1]

	out_dir = "Outputs/generated_time_series/"

	# GET REGIONS NAMES FOR THEIR CODES
	brain_areas_desc = pd. read_csv ("brain_areas.tsv", sep = '\t', header = 0)

	regions = []
	for num_region in args. regions:
		regions. append (brain_areas_desc . loc [brain_areas_desc ["Code"] == num_region, "Name"]. values [0])

	""" OUTPUT DIRECTORY FOT THE GENERATED TIME SERIES """
	for dirct in ["Outputs/generated_time_series", "Outputs/generated_time_series/speech", "Outputs/generated_time_series/video", "Outputs/generated_time_series/eyetracking"]:
		if not os.path.exists (dirct):
			os.makedirs (dirct)

	""" GENERATE MULTIMODAL TIME SERIES FROM RAW SIGNALS """
	if not args. predict:
		print ("0%")
	speech_left, speech = speech_features (args.pred_module_path, args.generate, "Outputs/generated_time_series/speech")
	if not args. predict:
		print ("33%")
	video = facial_features (args.pred_module_path, args.generate, "Outputs/generated_time_series/video", args.openface_path)
	if not args. predict:
		print ("33%")
	eyetracking = eyetracking_features (args.pred_module_path, args.generate, "Outputs/generated_time_series/eyetracking")
	if not args. predict:
		print ("100%")

	""" CONCATENATE MULTIMODAL DATA """
	all_data = np. concatenate ((speech_left. values, speech. values[:,1:], video. values[:,1:], eyetracking. values[:,1:]), axis = 1)
	columns = list (speech_left. columns) +  list (speech. columns [1:]) + list (video. columns [1:]) + list (eyetracking. columns [1:])

	# WRIGHT MULTIMODAL TIME SERIES TO CSV FILE
	pd. DataFrame (all_data, columns = columns). to_csv (out_dir + "all_features.csv", sep = ';', index = False)

	if args. predict:
		print ("0")
		lagged_names = []
		for col in columns [1: ]:
			lagged_names. extend ([col + "_t%d"%(p) for p in range (args. lag, 2, -1)])

		all_data = pd. DataFrame (toSuppervisedData (all_data, args. lag). data, columns = lagged_names)

		""" load the best models for each regions """
		if args. type == 'h':
			conversation_type = 'HH'
		elif args. type == 'r':
			conversation_type = 'HR'
		else:
			print ("Error in arguments, use -h for help!")
			exit (1)

		trained_models = glob. glob ("%s/trained_models/*%s.pkl"%(args.pred_module_path,conversation_type))

		# dictionary of predictions: results
		preds = {}
		predictors_variables = {}
		nb_r = 1
		for region in regions:
			predictors_data = pd. DataFrame ()
			predictors_data. columns = []
			fname = ""
			for filename in trained_models:
				if region in  filename:
					fname = filename
					break

			model_name = fname. split ('/')[-1]. split ('_') [0]
			#print (model_name)
			model = joblib.load (fname)

			predictors = literal_eval (get_predictors_dict (model_name, region, args. type, args.pred_module_path))
			#print ("Predictors time series: ", predictors, "\n -------------")

			predictors_data = all_data. loc [:, predictors]

			pred = model. predict (predictors_data)

			preds [region] = [0 for i in range (args. lag)] + pred. tolist ()
			predictors_variables [region] = literal_eval (get_predictors (model_name, region, args. type, args.pred_module_path))
			#print (region, "\n", 18 * '-')
			print (int (100 * float (nb_r) / len (regions)))
			nb_r += 1
		preds_var = pd.DataFrame ()
		for col in predictors_variables. keys ():
			preds_var[col] = [str (predictors_variables [col])]

		# time index : fMRI recording frequency
		step = 1.205
		index = [step]
		for i in range (1, args. lag + len (pred)):
			index. append (index [i - 1] + step)

		pd. DataFrame (preds, index = index). to_csv ("Outputs/predictions.csv", sep = ';', index_label = ["Time (s)"])
		preds_var. to_csv ("Outputs/predictors.csv", sep = ';', index = False)
