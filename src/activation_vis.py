'''
    Author: Youssef Hmamouche
    Year: 2019
    Generate video of brain activity predictions
    This script uses a csv file of predictions, and annotation files associated to brain parcellation
'''

import numpy as np
from visbrain.gui import Brain
from visbrain.objects import (BrainObj, SceneObj, SourceObj, ConnectObj)
from visbrain.io import download_file

import nibabel as nib
import pandas as pd
import os
import cv2
import argparse

#=================================================================#
def get_label_from_roi (brain_area, correspondance_tale):
    return correspondance_tale. loc [correspondance_tale["ShortName"] == brain_area, "Label"]. values [0]

#=================================================================#
def read_annot_file (file):
    annot_data = pd.DataFrame (nib.freesurfer.io.read_annot (l_file)). transpose ()
    annot_data. columns = ["Codes",  "Colors", "Labels"]
    return annot_data

#=================================================================#
def create_brain_obj (annot_file_R, annot_file_L, areas):
    brain_obj = BrainObj(name = 'inflated', hemisphere='both', translucent=False, cbtxtsz = 10., verbose = None) #, cblabel='Parcellates example', cbtxtsz=4.)
    left_areas = []
    right_areas = []

    for area in areas:
        if area[-1] == 'R':
            right_areas. append (area)
        elif area[-1] == 'L':
            left_areas. append (area)

    if len (left_areas) > 0:
        brain_obj.parcellize (annot_file_L, hemisphere='left',  select=left_areas)

    if len (right_areas) > 0:
        brain_obj.parcellize (annot_file_R, hemisphere='right',  select=right_areas)

    return brain_obj

#=================================================================#
def create_scene ():
    sc = SceneObj (size=(1400, 1000))
    brain_objs = []

    # CREATE 4 BRAIN OBJECTS EACH WITH SPECOFOC ROTATION
    brain_objs = []
    for rot in ["left", "right", 'side-fl', 'side-fr', 'front', 'back']:
        brain_objs. append (BrainObj(name = 'inflated', hemisphere='both', translucent=False, cbtxtsz = 10., verbose = None))

    sc.add_to_subplot(brain_objs[0], row=0, col=0, rotate='right', title='Right', zoom = 3.5)
    sc.add_to_subplot(brain_objs[1], row=0, col=1, rotate='left', title='Left')
    sc.add_to_subplot(brain_objs[2], row=1, col=0, rotate='top', title='Top')
    sc.add_to_subplot(brain_objs[3], row=1, col=1, rotate='bottom', title='Bottom')
    sc.add_to_subplot(brain_objs[4], row=2, col=0, rotate='front', title='Front')
    sc.add_to_subplot(brain_objs[5], row=2, col=1, rotate='back', title='Back')
    return sc, brain_objs


#=================================================================#
def add_activation (areas_labels, brain_objs, annot_file_R, annot_file_L):

    right_areas = []
    left_areas = []
    for area in areas_labels:
        if area[-1] == 'R':
            right_areas. append (area)
        elif area[-1] == 'L':
            left_areas. append (area)

    for i in range (len (brain_objs)):
        brain_objs[i] = BrainObj('inflated', hemisphere='both', translucent=False)
        if len (left_areas) > 0:
            brain_objs[i].parcellize (annot_file_L, hemisphere='left',  select=left_areas)

        if len (right_areas) > 0:
            brain_objs[i].parcellize (annot_file_R, hemisphere='right',  select=right_areas)


#=================================================================#
def add_objs_to_scene (sc, brain_objs):
    sc = SceneObj (size=(1400, 1000))
    sc.add_to_subplot(brain_objs[0], row=0, col=0, rotate='right', title='Right')
    sc.add_to_subplot(brain_objs[1], row=0, col=1, rotate='left', title='Left')
    sc.add_to_subplot(brain_objs[2], row=1, col=0, rotate='top', title='Top')
    sc.add_to_subplot(brain_objs[3], row=1, col=1, rotate='bottom', title='Bottom')
    sc.add_to_subplot(brain_objs[4], row=2, col=0, rotate='front', title='Front')
    sc.add_to_subplot(brain_objs[5], row=2, col=1, rotate='back', title='Back')
    return sc

#=================================================================#
if __name__ == '__main__':
    parser = argparse. ArgumentParser ()
    requiredNamed = parser.add_argument_group('Required arguments')
    requiredNamed. add_argument ('--input_dir','-in', help = "path of input directory")
    args = parser.parse_args()

    # read brain areas file
    brain_areas_csv = pd. read_csv ("brain_areas.tsv", sep = '\t', header = 0)
    coresp_table = brain_areas_csv[["ShortName", "Label"]]

    # read parrcelation files
    l_file = "parcellation/lh.BN_Atlas.annot"
    r_file = "parcellation/rh.BN_Atlas.annot"

    # set video parameters
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = 30
    out = cv2.VideoWriter ("%s/Outputs/brain_activation.mp4"%args.input_dir, fourcc, fps, (1400, 1000))

    # read the prediction file (fMRI responses predictions)
    predictions = pd.read_csv ("%s/Outputs/predictions.csv"%args.input_dir, sep = ';', header = 0)
    processed_brain_areas = list (predictions. columns[1:])

    # create scene of 6 brain objects
    scene, br_objs = create_scene ()

    # Brain visualisation of fMRI predictions
    for i in range (predictions. shape [0]):
        # find activated areas
        activated_areas_labels = []
        ligne = predictions. iloc [i, 1:]. values

        for j in range (len (ligne)):
            if ligne[j] == 1:
                activated_areas_labels. append (get_label_from_roi (processed_brain_areas[j], coresp_table))

        # add activation to the six brain objects
        add_activation (activated_areas_labels, br_objs, r_file, l_file)
        scene = add_objs_to_scene (scene, br_objs)
        # render image
        img = scene. render ()

        # Transform the image to RGB
        img = cv2.cvtColor (img, cv2.COLOR_BGR2RGB)

        # Write the image for a duration of 1.2s (we suupose that we have a prediction each 1.2s)
        # TODO: make this more general (detect the timing automatically from the prediction file)
        for j in range (36):
            out.write(img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()
    cv2.destroyAllWindows()
