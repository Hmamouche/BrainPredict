# coding: utf8
# Author: Youssef Hmamouche
# Year: 2020:
# Extracting simles as time series from video using opencv
# And resample the output according the BOLD signal frequency

import numpy as np
import pandas as pd
import cv2, dlib, sys, os, inspect, argparse

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
maindir = os.path.dirname(parentdir)

sys.path.insert (0, maindir)
import src.resampling as resampling
#==================================================
if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("video", help="the path of the video to process.")
	parser.add_argument("out_dir", help="the path where to store the results.")
	parser.add_argument("--demo",'-d', help = "If this script is using for demo.", action = "store_true")
	parser.add_argument("--show",'-s', help="Showing the video.", action="store_true")

	args = parser.parse_args()

	face_cascade = cv2.CascadeClassifier("src/utils/detection_models/haarcascades/haarcascade_frontalface_default.xml")
	smile_cascade = cv2.CascadeClassifier('src/utils/detection_models/haarcascades/haarcascade_smile.xml')

	if args. out_dir[-1] != '/':
	    args. out_dir += '/'

	# Input directory
	if args. demo:
	    conversation_name = "facial_features_smiles"
	else:
		# Input directory
		conversation_name = args. video.split ('/')[-1]. split ('.')[0]

	out_file = args. out_dir + conversation_name

	if os.path.isfile (out_file + ".pkl") and pd.read_pickle  (out_file + ".pkl"). shape [0] > 0:
		print ("Video already processed!")
		exit (1)

	# starting video streaming
	video_capture = cv2.VideoCapture(args.video)
	#video_capture = cv2.VideoCapture(0)

	# Frames frequence : fps frame per seconde
	fps = video_capture.get(cv2.CAP_PROP_FPS)
	length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

	# parameter initilization
	nb_frames = 0

	time_series = []
	current_time = 0

	j = 0
	while True:
		ret, bgr_image = video_capture.read()

		if ret == False:
		    break

		gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
		rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

		faces = face_cascade.detectMultiScale(gray_image, 1.1)

		# We suppose we have at most on face in each image
		if len (faces) > 0:
			face_cordinates = faces[0]
			(x, y, w, h) = faces[0]
			gray_face = gray_image [y:y + h, x:x + w]
			color_face = bgr_image [y:y + h, x:x + w]
			smiles = smile_cascade. detectMultiScale(gray_face, 1.8, 20)

			if len (smiles) > 0:
				time_series. append ([current_time, 1])
			else:
				time_series. append ([current_time, 0])

		else:
			time_series. append ([current_time, 0])

		current_time += 1.0 / fps

		if args. show:
			cv2.rectangle (bgr_image, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
			for (sx, sy, sw, sh) in smiles:
				cv2.rectangle (color_face, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
			cv2. imshow ('Video', bgr_image)

		if cv2.waitKey(100) & 0xFF == ord('q'):
			break


	# Index according to fRMI recording step
	index = [1.205]
	i = 1
	while (1.205 + index [i - 1] < current_time):
		index. append (1.205 + index [i - 1])
		i += 1


	time_series = resampling. resample_ts (np. array (time_series), index, mode = "mode")

	df = pd. DataFrame (time_series, columns = ["Time (s)", "Smiles_I"])
	df. to_pickle (out_file + '.pkl')
