# coding: utf8

#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spacy as sp
import tools.tools as ts
import glob
import os,sys,inspect
import argparse


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
maindir = os.path.dirname(parentdir)

sys.path.insert(0,'%s/src/utils/SPPAS'%maindir)
sys.path.insert(3,maindir)
import src.utils.SPPAS.sppas.src.anndata.aio.readwrite as spp


#-----------------------------------------------------------------------------
OK_FORMS = [u"o.k.",u"okay",u"ok",u"OK",u"O.K."]
VOILA_FORMS = [u"voilà",u"voila"]
DACCORD_FORMS = [u"d'accord",u"d' accord"]
LAUGHTER_FORMS = [u'@',u'@ @',u'@@']
EMO_FORMS = [u'@',u'@ @',u'@@',u'ah',u'oh']

REGULATORY_DM_SET = set([u"mh",u"ouais",u"oui",u"o.k.",u"okay",u"ok",u"OK",u"O.K.",u"d'accord",u"voilà",u"voila",u'bon',u"d'",
u"accord",u'@',u'@ @',u'@@',u'non',u"ah",u"euh",u'ben',u"et",u"mais",u"*",u"heu",u"hum",u"donc",u"+",u"eh",u"beh",u"donc",u"oh",u"pff",u"hein"])

SILENCE = [u'+',u'#',u'',u'*', u'***']
FILLED_PAUSE_ITEMS = [u"euh",u"heu",u"hum",u"mh"]
LAUGHTER = [u'@',u'@@']
MAIN_FEEDBACK_ITEMS = [u"mh",u"ouais",u"oui",u'non',u'ah',u"mouais"]+ OK_FORMS + VOILA_FORMS + DACCORD_FORMS + LAUGHTER_FORMS
MAIN_DISCOURSE_ITEMS = [u"alors",u"mais",u'et',u'puis',u'enfin',u'parceque',u'parcequ',u'ensuite']
MAIN_PARTICLES_ITEMS = [u"quoi",u"hein",u"bon",u'mais',u'ben',u'beh',u'enfin',u'vois',u'putain',u'bref', u'bah']

ALL_ITEMS = FILLED_PAUSE_ITEMS + LAUGHTER + MAIN_FEEDBACK_ITEMS + MAIN_DISCOURSE_ITEMS + MAIN_PARTICLES_ITEMS

MAIN_FEEDBACK_ITEMS_ENG = [u"mh",u"yes",u"yeah",u'no',u'ah']+ OK_FORMS  + [u"right"] + LAUGHTER_FORMS
MAIN_DISCOURSE_ITEMS_ENG = [u"so",u"but",u"therefore",u'and',u'then',u'finally',u'because',u'after']
MAIN_PARTICLES_ITEMS_ENG = [u"what",u"hein",u"well",u'but',u'ben',u'finally',u'short']
ALL_ITEMS_ENG = FILLED_PAUSE_ITEMS + LAUGHTER + MAIN_FEEDBACK_ITEMS_ENG + MAIN_DISCOURSE_ITEMS_ENG + MAIN_PARTICLES_ITEMS_ENG

colors = ["black", "darkblue", "brown", "red", "slategrey", "darkorange", "grey","blue", "indigo", "darkgreen"]


#-----------------------------------------------------------------------------
def get_intervals (ts):
	y = []
	for i in range (0, len (ts[0]) - 1):
		if (ts[1][i] == 1 and ts[1][i+1] == 1):
			y.append ( [ts[0][i], ts[0][i + 1]] )
	return y

#---------------------------------------------------------------------
# Get nearest index point in vect to the the value 'value'
def nearestPoint (vect, value):
	index = -1
	for i in range (len (vect) - 1):
		if value >= vect [i] and value < vect [i + 1]:
			index = i
			break
	if value == vect[-1]:
		index = len (vect) - 1
	return index

#---------------------------------------
# Get points from the time series ts that correspond to index axis
# two modes are available: the sum or the mean of points in previous interval
def sample_cont_ts (ts, axis, mode = 'mean'):
	set_of_points = [[] for x in range (len (axis))]
	y = [0 for x in range (len (axis))]

	if len (ts) < 2:
		return y
	if len (ts[0]) == 0 or len (ts [1]) == 0:
		return y
	for i in range (len (ts [0])):
		for j in range (0, len (axis)):
			if j == 0:
				if ((0 <= ts [0][i]) and (axis [j] >= ts [0][i])):
					set_of_points [j]. append (ts [1][i])
					break
			else:
				if ((axis [j - 1] < ts [0][i]) and (axis [j] >= ts [0][i])):
					set_of_points [j]. append (ts [1][i])
					break

	if mode == 'mean':
		for j in range (0, len (y)):
			if len (set_of_points[j]) > 0:
				y[j] = np.mean (set_of_points[j])

	elif mode == 'max':
		for j in range (0, len (y)):
			if len (set_of_points[j]) > 0:
				y[j] = np.max (set_of_points[j])

	elif mode == 'sum':
		for j in range (0, len (y)):
			if len (set_of_points[j]) > 0:
				y[j] = np.sum (set_of_points[j])

	elif mode == 'binary':
		for j in range (0, len (y)):
			if sum (set_of_points[j]) > 0:
				y[j] = 1
			else:
				y [j] = 0

	return y

#================================================================
""" intersection between two intervals """
def get_intersection (A, B):

	overlap = [0, 0]
	if A[1] <= B[0] or B[1] <= A[0]:
		return []
	else:
		overlap = [max (A[0], B[0]), min (A[1], B[1])]
	return overlap

#================================================================
# quantize time series
# step : the step between two observarions
# nb_obs : the number of observations
# axis : discrete vector
# discretization method: each value atributed represent the percentage of the variable represented by bins in each succesive steps of the discrete index

def sample_square (ts, axis):
	axis_intervals = []

	for i in range (len (axis)):
		if i == 0:
			axis_intervals. append ([0, axis[i] ])
		else:
			axis_intervals. append ([axis[i-1], axis[i] ])

	y = [0 for i in range (len (axis))]

	if len (ts) == 0:
		return y

	# Compute the duration in each interval of the axis
	i = 0
	for inter_ax in axis_intervals:
		step = inter_ax [1] - inter_ax [0]
		for interval in ts:
			overlap = get_intersection (inter_ax, interval)

			if len (overlap) > 0:
				y [i] += (overlap [1] - overlap [0]) / step
		i += 1

	return y

#================================================================
if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("data_dir", help="the path of the file to process.")
	parser.add_argument("out_dir", help="the path where to store the results.")
	parser.add_argument("--language", "-lg", default = "fr", choices = ["fr", "eng"], help="Language.")
	parser.add_argument("--left", "-l", help="Process participant speech.", action="store_true")
	parser.add_argument("--outname", "-n", help="Rename output file names by default.", action="store_true")

	args = parser.parse_args()

	data_dir = args. data_dir
	out_dir = args. out_dir

	if args. out_dir[-1] != '/':
		args. out_dir += '/'

	# Get video conversation
	audio_path = glob.glob ("%s/*.wav"%data_dir)[0]


	# create output dir file if does not exist
	if not os.path.exists (args. out_dir):
		os.makedirs (args. out_dir)

	filename = args. data_dir.split('/')[-1]. split ('.')[0]

	conversation_name = data_dir.split ('/')[-1]

	if conversation_name == "" or args.outname:
		if args. left:
			conversation_name = "speech_features_left"
		else:
			conversation_name = "speech_features"

	output_filename_pkl = out_dir +  conversation_name + ".pkl"


	# exit if conversation already processed
	if os.path.isfile (output_filename_pkl):
		print ("Conversation already processed")
		exit (1)

	# Read audio, and transcription file
	for file in glob.glob(data_dir + "/*"):
		if "left" in file and ".TextGrid" in file and "palign.textgrid" not in file:
			transcription_left = file
		elif "right" in file and ".TextGrid" in file and "palign.textgrid" not in file:
			transcription_right = file

		elif "right" in file and  "palign.textgrid" in file:
			transcription_right_palign = file

		elif "left" in file and  "palign.textgrid" in file:
			transcription_left_palign = file

		elif "left" in file and  ".wav" in file:
			left_wav_file = file

		elif "right" in file and  ".wav" in file:
			right_wav_file = file

	# Select language
	if args. language == "fr":
		nlp = sp.load('fr_core_news_sm')
	elif args. language == "eng":
		nlp = sp.load('en_core_web_sm')

	# Read TextGrid files
	# get the left part of the transcription

	parser = spp.sppasRW (transcription_left)
	tier_left = parser.read(). find ("Transcription")
	if  tier_left is None:
		tier_left = parser.read(). find ("IPUs")

	# get the right part of the transcription
	parser = spp.sppasRW (transcription_right)
	tier_right = parser.read(). find ("Transcription")
	if  tier_right is None:
		tier_right = parser.read(). find ("IPUs")

	if args.left:
		tier = tier_left
		min_ipu = 0.2
		wav_file = left_wav_file
	else:
		tier = tier_right
		min_ipu = 0.2
		wav_file = right_wav_file

	# IPU
	IPU, _ = ts. get_ipu (tier, 1)

	# Get get audio duration
	for sppasOb  in tier:
		_, [start, stop], _ = ts. get_interval (sppasOb)

	# fMRI Index variable
	physio_index = [1.205]
	i = 1
	while (1.205 + physio_index [i - 1] < stop):
		physio_index. append (1.205 + physio_index [i - 1])
		i += 1

	#disc_SpeechActivity = sample_square (SpeechActivity, physio_index)
	discretized_ipu_1 = sample_square (IPU, physio_index)

	for i in range (len (discretized_ipu_1)):
		if discretized_ipu_1 [i] < min_ipu:
			discretized_ipu_1 [i] = 0
		else:
			discretized_ipu_1 [i] = 1

	# Joint Laugh: laugh overlap
	#joint_laugh = ts. get_joint_laugh (tier_left, tier_right, LAUGHTER_FORMS)

	# recation time
	if args. left:
		reaction_time = ts. get_reaction_time (tier_right, tier_left)
	else:
		reaction_time = ts. get_reaction_time (tier_left, tier_right)

	# Lexical richness
	richess_lex1 = ts.generate_RL_ts (tier, nlp, "meth1")
	richess_lex2 = ts.generate_RL_ts (tier, nlp, "meth2")

	speech_rate = ts.get_speech_rate (tier, nlp)

	# Time of Filled breaks, feed_backs
	# aligment
	try:
		if args.left:
			parser = spp.sppasRW (transcription_left_palign)
			tier_align = parser.read(). find ("TokensAlign")

		else:
			parser = spp.sppasRW (transcription_right_palign)
			tier_align = parser. read(). find ("TokensAlign")

	except:
		print ("error in conversation %s"%(output_filename_pkl))
	# Time of Filled breaks, feed_backs
	if args. language == "fr":
		filled_breaks = ts. get_items_existence (tier_align, list_of_tokens =  FILLED_PAUSE_ITEMS)
		main_feed_items = ts. get_items_existence (tier_align, list_of_tokens =  MAIN_FEEDBACK_ITEMS)
		main_discourse_items = ts. get_items_existence (tier_align, list_of_tokens =  MAIN_DISCOURSE_ITEMS)
		laughters = ts. get_items_existence (tier_align, list_of_tokens =  LAUGHTER_FORMS)
		main_particles_items = ts. get_items_existence (tier_align, list_of_tokens =  MAIN_PARTICLES_ITEMS)
		socio_items = ts. get_items_existence (tier_align, list_of_tokens =  ALL_ITEMS)
		# handle particle items separately as continuous time series
		#main_particles_items = ts. get_particle_items (tier, nlp, list_of_tokens =  MAIN_PARTICLES_ITEMS)

	elif args. language == "eng":
		filled_breaks = ts. get_items_existence (tier_align, list_of_tokens =  FILLED_PAUSE_ITEMS)
		main_feed_items = ts. get_items_existence (tier_align, list_of_tokens =  MAIN_FEEDBACK_ITEMS_ENG)
		main_discourse_items = ts. get_items_existence (tier_align, list_of_tokens =  MAIN_DISCOURSE_ITEMS_ENG)
		laughters = ts. get_items_existence (tier_align, list_of_tokens =  LAUGHTER_FORMS)
		main_particles_items = ts. get_items_existence (tier, list_of_tokens =  MAIN_PARTICLES_ITEMS_ENG)
		# handle particle items separately as continuous time series """
		#main_particles_items = ts. get_particle_items (tier, nlp, list_of_tokens =  MAIN_PARTICLES_ITEMS_ENG)

	x_emotions, polarity, subejctivity = ts. emotion_ts_from_text (tier, nlp)

	# Overlap
	if args. left:
		overlap = []
	else:
		overlap = ts. get_overlap (tier_left, tier_right)

	# Time series dictionary
	time_series = {
				"IPU": IPU,
				"disc_IPU": discretized_ipu_1,
				"Overlap": overlap,
				"ReactionTime":reaction_time,
				"FilledBreaks":filled_breaks,
				"Feedbacks":main_feed_items,
				"Discourses":main_discourse_items,
				"Particles":main_particles_items,
				"Laughters":laughters,
				"UnionSocioItems":socio_items,
				"LexicalRichness":richess_lex2,
				"TypeTokenRatio":richess_lex1,
				"SpeechRate": speech_rate,
 				"Polarity": [x_emotions, polarity],
				"Subjectivity": [x_emotions, subejctivity],
				}

	#labels = list (time_series. keys ())
	labels = ["IPU", "disc_IPU", "Overlap", "ReactionTime", "FilledBreaks", "Feedbacks", "Discourses", "Particles", "Laughters"\
			  ,"UnionSocioItems", "LexicalRichness", "TypeTokenRatio", "SpeechRate", "Polarity", "Subjectivity"]

	if args.left:
		# no need for overlap for bothe converssants
		labels. remove ("Overlap")

	markers = ['.' for i in range (len (labels))]

	df = pd.DataFrame (index = physio_index)

	# Conbstruct a dataframe with smapled time serie according to the physio index
	df["Time (s)"] = physio_index
	#df ["Silence"] = silence
	for label in labels [:]:
		if label in ["disc_IPU", "disc_SpeechActivity", "disc_IPU2", "disc_IPU3", "disc_IPU4"]:
			df [label] = time_series [label]

		elif (label in ["Silence", "IPU", "SpeechActivity", "Overlap", "joint_laugh"]):
			df [label] = sample_square (time_series [label], physio_index)


		elif label in ["Particles", "Discourses", "FilledBreaks", "Laughters", "Feedbacks", "UnionSocioItems"]:
			df [label] = sample_cont_ts (time_series [label], physio_index, mode = "binary")

		else:
			if label == "Signal":
				df [label] = ts. normalize (sample_cont_ts (time_series [label], physio_index))
			else:
				df [label] = sample_cont_ts (time_series [label], physio_index)

	if args.left:
		for i in range (len (labels)):
			labels [i] += "_P"
	else:
		for i in range (len (labels)):
			labels [i] += "_I"
	df. columns = ["Time (s)"] + labels

	# save data
	df.to_pickle(output_filename_pkl)
