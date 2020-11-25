"""
	Author: Youssef Hmamouche
	Year: 2019
	Generate time series from raw signals: video audio, and eyetracking coordiantes.
"""

import os
import glob
import pandas as pd
import numpy as np
import argparse
from ast import literal_eval
import sys

#---------------------------------------------------#
'''def get_predictors (model_name, region, type, path):
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

	return predictors'''

#---------------------------------------------------#
def speech_features (out_dir, language):
	"""
	generate speech features from audio files
	compute_features: logical, for computing the features or not (if they alreadu exists)
	out_dir: output directory
	"""

	audio_input = "%s/Inputs/speech"%out_dir
	audio_output = "%s/Outputs/generated_time_series/speech"%out_dir

	if os.path.exists ("%s/speech_features.pkl"%audio_output) and os.path.exists ("%s/speech_features_left.pkl"%audio_output):
		print ("Speech already processing!")
		speech = pd. read_pickle ("%s/speech_features.pkl"%audio_output)
		speech_left = pd. read_pickle ("%s/speech_features_left.pkl"%audio_output)
		return speech_left, speech

	if language == "fr":
		lang = "fra"
	elif language == "eng":
		lang = "eng"

	os. system ("python src/utils/SPPAS/sppas/bin/normalize.py -r src/utils/SPPAS/resources/vocab/eng.vocab -I %s  -l %s -e .TextGrid --quiet"%(audio_input, lang))
	os. system ("python src/utils/SPPAS/sppas/bin/phonetize.py  -I %s -l %s -e .TextGrid"%(audio_input, lang))
	os. system ("python src/utils/SPPAS/sppas/bin/alignment.py  -I %s -l %s -e .TextGrid --aligner basic"%(audio_input, lang))

	out = os. system ("python src/generate_ts/speech_features.py %s %s/ -lg %s -n"%(audio_input, audio_output, language))
	out = os. system ("python src/generate_ts/speech_features.py %s %s/ -l -lg %s -n"%(audio_input, audio_output, language))

	if out_dir[-1] != '/':
		out_dir += '/'
	speech = pd. read_pickle ("%s/speech_features.pkl"%audio_output)
	speech_left = pd. read_pickle ("%s/speech_features_left.pkl"%audio_output)
	return speech_left, speech

#---------------------------------------------------#
def openface_features (out_dir, openface_path):
	""" extract facial features with openface from interlocutor video  """

	#video_input = "%s/Inputs/video"%out_dir
	video_output = "%s/Outputs/generated_time_series/openface/"%out_dir
	video_path = glob.glob ("%s/Inputs/video/*.avi"%out_dir)

	facial_output = "%s/Outputs/generated_time_series/openface/"%out_dir

	if len (video_path) == 0:
		print ("Error: there is no input video!")
		exit (1)
	else:
		video_path = video_path[0]

	video_name = video_path. split ('/')[-1]. split ('.')[0]

	if out_dir[-1] != '/':
		out_dir += '/'

	os. system ("python src/generate_ts/openface_features.py %s %s -op %s"%(video_path, video_output, openface_path))


#---------------------------------------------------#
def extra_features (out_dir, type = "eyetracking"):
	""" eyetracking data """

	video_output = "%s/Outputs/generated_time_series/openface"%out_dir
	pickle_output = "%s/Outputs/generated_time_series/%s"%(out_dir, type)
	video_path = glob.glob ("%s/Inputs/video/*.avi"%out_dir)
	if len (video_path) == 0:
		print ("Error: there is no input video!")
		exit (1)
	else:
		video_path = video_path [0]

	if out_dir[-1] != '/':
		out_dir += '/'

	try:
		openface_features = glob.glob (video_output + "/*.pkl") [0]
	except:
		print ("\nFile error: Openface features not found.")
		exit (1)

	if type == "eyetracking":
		try:
			eyelink_output_file = glob.glob ("%s/Inputs/eyetracking/*.txt"%out_dir)[0]
		except:
			print ("Error, there is no eyetracking .txt file in the inputs!")
			exit (1)
		os. system ("python src/read_eyelink_data.py %s %sOutputs/generated_time_series/eyetracking/"%(eyelink_output_file, out_dir))

		try:
			gaze_coordinates_file = glob.glob ("%s/Outputs/generated_time_series/eyetracking/*.pkl"%out_dir)[0]
		except:
			print ("Error, there is no eyetracking pkl file in the outputs!")
			exit (1)

		out = os. system ("python src/generate_ts/eyetracking.py %s %s -d -eye %s -faf %s -sv"%(video_path, pickle_output, gaze_coordinates_file, openface_features))

	elif type == "emotions":
		out = os. system ("python src/generate_ts/facial_emotions.py -d %s %s"%(video_path, pickle_output))

	elif type == "facial":
		out = os. system ("python src/generate_ts/facial_features.py %s %s -d -faf %s"%(video_path, pickle_output, openface_features))

	elif type == "smiles":
		out = os. system ("python src/generate_ts/dlib_smiles.py -d %s %s"%(video_path, pickle_output))


	out_filename = glob.glob ("%s/*.pkl"%pickle_output)[0]

	return pd. read_pickle (out_filename)

#---------------------------------------------------#
if __name__ == '__main__':
	parser = argparse. ArgumentParser ()
	requiredNamed = parser.add_argument_group('Required arguments')
	requiredNamed. add_argument ('--regions','-rg', help = "Numbers of brain areas to predict (see brain_areas.tsv)", nargs = '+', type=int)
	requiredNamed.add_argument("--language", "-lg", default = "fr", choices = ["fr", "eng"], help="Language.")
	requiredNamed. add_argument ('--openface_path','-ofp', help = "path of Openface", required=True)
	requiredNamed. add_argument ('--input_dir','-in', help = "path of input directory", required=True)
	args = parser.parse_args()

	out_dir =  "%s/Outputs/generated_time_series/"%args.input_dir

	# GET REGIONS NAMES FOR THEIR CODES
	brain_areas_desc = pd. read_csv ("brain_areas.tsv", sep = '\t', header = 0)

	regions = []
	for num_region in args. regions:
		regions. append (brain_areas_desc . loc [brain_areas_desc ["Code"] == num_region, "Name"]. values [0])

	# CREATE OUTPUT DIRECTORIES FOR EACH TYPE OF TIME SERIES
	for dirct in ["%s/Outputs"%args.input_dir, out_dir, "%s/Outputs/generated_time_series/speech"%args.input_dir, \
				 "%s/Outputs/generated_time_series/openface"%args.input_dir, \
				 "%s/Outputs/generated_time_series/eyetracking"%args.input_dir,\
				 "%s/Outputs/generated_time_series/emotions"%args.input_dir,\
				 "%s/Outputs/generated_time_series/facial"%args.input_dir,\
				 "%s/Outputs/generated_time_series/smiles"%args.input_dir\
				 ]:
		if not os.path.exists (dirct):
			os.makedirs (dirct)

	# GENERATE MULTIMODAL TIME SERIES FROM RAW SIGNALS
	speech_left, speech = speech_features (args.input_dir, args. language)
	print ("Processing speech features, ... Done.")
	openface_features (args.input_dir, args.openface_path)
	print ("Processing openface features, ... Done.")

	# EXTRACT OTHER FACIAL FEATURES: EMOTIONS, ROTATIONAL AND TRANSATION HEAD ENERGY, FACE LOOKS ...
	eyetracking = extra_features (args.input_dir, "eyetracking")
	print ("Processing eyetracking, ... Done.")
	emotions = extra_features (args.input_dir, "emotions")
	print ("Processing emotions, ... Done.")
	facial = extra_features (args.input_dir, "facial")
	print ("Processing facial features, ... Done.")
	smiles = extra_features (args.input_dir, "smiles")
	print ("Processing smiles, ... Done.")

	min_obs = min (speech_left. shape[0], speech_left. shape[0], eyetracking. shape[0], emotions. shape[0], facial. shape[0], smiles. shape[0])
	# CONCATENATE AND SAVE MULTIMODAL DATA
	all_data = np. concatenate ((speech_left. values[:min_obs,:],speech. values[:min_obs,1:], eyetracking. values[:min_obs,1:], emotions. values[:min_obs,1:], facial. values[:min_obs,1:], smiles. values[:min_obs,1:]), axis = 1)
	columns = list (speech_left. columns) +  list (speech. columns [1:]) + list (eyetracking. columns [1:]) + list (emotions. columns [1:]) + list (facial. columns [1:]) + list (smiles. columns [1:])
	pd. DataFrame (all_data, columns = columns). to_csv (out_dir + "all_features.csv", sep = ';', index = False)
