import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from celluloid import Camera
from ast import literal_eval
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib.ticker as ticker
import nibabel as nib
import matplotlib as mpl

import argparse

def df_from_parccelation_file (l_annot_file, r_annot_file):
	annot_l = pd.DataFrame (nib.freesurfer.io.read_annot (l_annot_file)). transpose ()
	annot_l. columns = ["Code", "Color", "Label"]
	annot_l["Label"] = annot_l["Label"].str.decode("utf-8")

	annot_r = pd.DataFrame (nib.freesurfer.io.read_annot (r_annot_file)). transpose ()
	annot_r. columns = ["Code", "Color", "Label"]
	annot_r["Label"] = annot_r["Label"].str.decode("utf-8")

	return annot_l, annot_r

#================================================
def create_figure (rois, index):
	# SAVE PREDICTIONS AS A VIDEO
	fig, ax = plt.subplots (nrows = len (rois), ncols = 1, figsize=(8.1,5.6),  sharex=True)
	fig.text(0.5, 0.04, 'Time (s)', ha='center')
	fig.subplots_adjust(
	    top=0.981,
	    bottom=0.09,
	    left=0.03,
	    right=0.88,
	    hspace=0.2,
	    wspace=0.2
	)
	for j in range (len (rois)):
		ax [j]. set_xlim (np.min (index), np. max (index) + 1)
		ax [j]. xaxis.set_minor_locator(MultipleLocator(5))
		ax [j]. set_ylim (0, 1.1)
		ax [j].yaxis. set_major_locator (ticker. MultipleLocator (1))

	return fig, ax

#================================================
def get_colors_from_parcellation (rois):

	brain_areas_tsv = pd. read_csv ("brain_areas.tsv", sep = '\t', header = 0)
	annot_l, annot_r = df_from_parccelation_file ("parcellation/lh.BN_Atlas.annot", "parcellation/rh.BN_Atlas.annot")

	# get colors of the predicted rois
	colors_of_rois =  []
	for region in predicted_rois:
		label = brain_areas_tsv. loc [brain_areas_tsv ["ShortName"] == region, "Label"]. values [0]
		if label[-1] in ['l', 'L']:
			color = annot_l. loc [annot_l ["Label"] == label,  "Color"]. values [0][0:4]
		else:
			color = annot_r. loc [annot_l ["Label"] == label,  "Color"]. values [0][0:4]

		# scale RGBA color into [0, 1]
		color = [float (a) / 255  for a in color]
		colors_of_rois. append (color)
	return colors_of_rois
#================================================
if __name__ == '__main__':

	parser = argparse. ArgumentParser ()
	requiredNamed = parser.add_argument_group('Required arguments')
	requiredNamed. add_argument ('--input_dir','-in', help = "path of input directory")
	args = parser.parse_args()

	# read predictions
	predictions = pd. read_csv ("%s/Outputs/predictions.csv"%args.input_dir, sep = ';', header = 0, index_col = 0)
	predicted_rois = list (predictions. columns)
	index = predictions. index
	predictions = predictions. values

	# read bold signal frequency from prediction file (which determine the predtcion time step)
	time_step = index[1] - index[0]

	# get colors of roi from parcellation files
	colors_of_rois = get_colors_from_parcellation (predicted_rois)

	# set seaborn style for the axis
	mpl.style.use('seaborn')

	# create figure with axis for each roi
	fig, ax = create_figure (predicted_rois, index)

	# connect the camera to the figure
	camera = Camera(fig)

	# record the images
	for i in range (1,len (index)):
		for j in range (len (predicted_rois)):
			ax[j]. plot (index [:i], predictions[:i, j], linewidth = 3, color = colors_of_rois [j], alpha = 1, label = predicted_rois[j])
			ax[j]. legend(['%s'%predicted_rois[j]], bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.05, markerscale = 0.5, handlelength=0.5, fontsize = 14)
		camera. snap()

	# save the animation as a video
	anim = camera.animate (repeat = False, interval = int (time_step * 1000))
	anim.save("%s/Outputs/predictions_video.mp4"%args.input_dir, extra_args=['-vcodec', 'h264', '-pix_fmt', 'yuv420p'])
	fig. savefig ("%s/Outputs/predictions.png"%args.input_dir)
