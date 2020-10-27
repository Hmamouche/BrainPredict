'''
    Author: Youssef Hmamouche
    Year: 2019
    Generate video of brain activity predictions
    This script uses a csv file of predictions, and annotation files for brain parcellation
'''

import numpy as np
from visbrain.gui import Brain
from visbrain.objects import (BrainObj, SceneObj, SourceObj, ConnectObj)

import nibabel as nib
import pandas as pd
import os, glob, argparse, cv2

#=================================================================

def get_label_from_roi (brain_area, correspondance_tale):
    return correspondance_tale. loc [correspondance_tale["ShortName"] == brain_area, "Label"]. values [0]

#=================================================================
def create_brain_obj (annot_file_R, annot_file_L, areas):
    brain_obj = BrainObj(name = 'inflated', hemisphere='both', translucent=False, cbtxtsz = 10.) #, cblabel='Parcellates example', cbtxtsz=4.)
    left_areas = []
    right_areas = []

    for area in  areas:
        if area[-1] in ['R', 'r']:
            right_areas. append (area)
        elif area[-1] in ['L', 'l']:
            left_areas. append (area)
        else:
            raise ("Error, label area does indicate if it is in left or rights hemisphere.")

    if len (left_areas) > 0:
        brain_obj.parcellize(annot_file_L, hemisphere='left',  select=left_areas)

    if len (right_areas) > 0:
        brain_obj.parcellize(annot_file_R, hemisphere='right',  select=right_areas)

    return brain_obj

#=================================================================
def render_image (areas_labels, annot_file_R, annot_file_L):

    CBAR_STATE = dict(cbtxtsz=12, txtsz=10., width=.1, cbtxtsh=3., rect=(-.3, -2., 1., 4.))
    KW = dict(title_size=14., zoom=0.5)
    obj = BrainObj('inflated', hemisphere='both', translucent=False, _scale = 1.5)
    annot_data_L = obj. get_parcellates (annot_file_L)
    annot_data_R = obj. get_parcellates (annot_file_R)
    select = []

    sc = SceneObj (size=(1400, 1000))
    brain_objs = []

    # CREATE 4 BRAIN OBJECTS EACH WITH SPECOFOC ROTATION
    for rot in ["left", "right", 'side-fl', 'side-fr', 'front', 'back']:
        brain_objs. append (create_brain_obj (annot_file_R, annot_file_L, areas_labels))

    # PLOT OBJECTS
    sc.add_to_subplot(brain_objs[0], row=0, col=0, rotate='right', title='Right')
    sc.add_to_subplot(brain_objs[1], row=0, col=1, rotate='left', title='Left')
    sc.add_to_subplot(brain_objs[2], row=1, col=0, rotate='top', title='Top')
    sc.add_to_subplot(brain_objs[3], row=1, col=1, rotate='bottom', title='Bottom')
    sc.add_to_subplot(brain_objs[4], row=2, col=0, rotate='side-fl', title='Front-left')
    sc.add_to_subplot(brain_objs[5], row=2, col=1, rotate='side-fr', title='Front-right')

    #sc.preview()
    #exit (1)
    return sc. render ()

"""================================================================="""
def render_brain_image (r_areas_labels, l_areas_labels, r_file, l_file):

    CBAR_STATE = dict(cbtxtsz=12, txtsz=10., width=.1, cbtxtsh=3., rect=(-.3, -2., 1., 4.))
    KW = dict(title_size=14., zoom=3)

    obj = BrainObj('inflated', hemisphere='both', translucent=False) #, cblabel='Parcellates example', cbtxtsz=4.)

    annot_data_l = obj. get_parcellates (l_file)
    annot_data_r = obj. get_parcellates (r_file)

    select_left = []
    select_right = []

    for l_area in l_areas_labels:
        select_left. append (annot_data_l ["Labels"]. loc[annot_data_l["Labels"] == l_area]. values)

    for r_area in r_areas_labels:
        select_right. append (annot_data_r ["Labels"]. loc[annot_data_r["Labels"] == r_area]. values)

    sc = SceneObj ()
    brain_objs = []

    # CREATE 4 BRAIN OBJECTS EACH WITH SPECOFOC ROTATION
    for rot in ["left", "right", 'side-fl', 'side-fr', 'front', 'back']:
        brain_objs. append (create_brain_obj (r_file, l_file, select_right, select_left))

    # PLOT OBJECTS
    sc.add_to_subplot(brain_objs[0], row=0, col=0, rotate='right', title='Right', zoom = 3)
    sc.add_to_subplot(brain_objs[1], row=0, col=1, rotate='left', title='Left', **KW)
    sc.add_to_subplot(brain_objs[2], row=1, col=0, rotate='side-fl', title='side-fl', **KW)
    sc.add_to_subplot(brain_objs[3], row=1, col=1, rotate='side-fr', title='side-fr', **KW)
    sc.add_to_subplot(brain_objs[4], row=2, col=0, rotate='front', title='front', **KW)
    sc.add_to_subplot(brain_objs[5], row=2, col=1, rotate='back', title='back', **KW)

    return sc. render ()

#=================================================================
def get_fps_from_input_video (video_path):
    """ get number of frames per seconde from a video """
    if not os.path.exists (video_path):
        raise ("Can't get fps from vide, video path does not exist.")

    video_capture = cv2.VideoCapture(video_path)

    return video_capture.get (cv2.CAP_PROP_FPS)

#=================================================================
if __name__ == '__main__':
    parser = argparse. ArgumentParser ()
    requiredNamed = parser.add_argument_group('Required arguments')
    requiredNamed. add_argument ('--input_dir','-in', help = "path of input directory")
    args = parser.parse_args()

    # file containing brain areas names and corresponding labels
    brain_areas_tsv = pd. read_csv ("brain_areas.tsv", sep = '\t', header = 0)


    # parcellation files
    l_file = "parcellation/lh.BN_Atlas.annot"
    r_file = "parcellation/rh.BN_Atlas.annot"

    # read predictions
    predictions = pd.read_csv ("%s/Outputs/predictions.csv"%args.input_dir, sep = ';', header = 0)
    predicted_areas = list (predictions. columns[1:])
    predictions = predictions. values

    # read bold signal frequency from prediction file (which determine the predtcion time step)
    time_step = predictions[1,0] - predictions[0,0]

    # input and output videos parameters
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_path = glob. glob ("%s/Inputs/video/*"%args. input_dir)[0]
    fps = get_fps_from_input_video (video_path)
    out = cv2.VideoWriter ("%s/Outputs/brain_activation.mp4"%args.input_dir, fourcc, fps, (1400, 1000))

    # create visualisations depending on the brain activity predictions
    for i in range (predictions. shape [0]):
        activated_areas = []
        regions = []
        ligne = predictions [i, 1:]

        for j in range (len (ligne)):
            if ligne[j] == 1:
                activated_areas. append (get_label_from_roi (predicted_areas[j], brain_areas_tsv))
                regions. append (predicted_areas[j])

        img = render_image (activated_areas, r_file, l_file)
        img = cv2.cvtColor (img, cv2.COLOR_BGR2RGB)

        # number of images in eac time step
        nb_images = int (fps*time_step)
        for j in range (nb_images):
            out.write(img)

    out.release()
    cv2.destroyAllWindows()
