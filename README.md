<!--- ## Introduction --->
## Introduction
A tool for predicting and visualizing the fMRI brain activity during bidirectional conversations of type human-human or human-machine.


## Dependencies
  * python>=3.6
  * Openface is required (https://github.com/TadasBaltrusaitis/OpenFace) to compute facial features from videos.


## Demo: using Qt Creator Interface
The working directory must be specified and must contain an Inputs folder containing speech, eyetracking, and video folders.

  ```bash
  ./BrainPredict
  ```

## Demo: using the command line
  * To run a demo, we need a video file (of the interlocutor), and the audios of both the participant and the interlocutor, and an eyetracking file of the participant.

  * A example is provided in the folder "Demo". To run the example:

  ```bash
  # Generate time series
  python src/predict.py -rg 1 2 3 4 5 6 -t r -ofp "path_to_openface" -pmp PredictionModule -in Demo -g
  # Make predictions
  python src/predict.py -rg 1 2 3 4 5 6 -t r -ofp "path_to_openface" -pmp PredictionModule -in Demo -p
  # Generate animated prediction in video from the obtained predictions
  python src/animation.py -in Demo
  # Using visbrain to visualize the predictions in the brain
  python src/visualization.py -in Demo

  --regions REGIONS [REGIONS ...], -rg REGIONS [REGIONS ...]
  --type TYPE, -t TYPE  conversation type (human or robot)
  --openface_path OPENFACE_PATH, -ofp OPENFACE_PATH
                         path of Openface
   -pred_module_path PRED_MODULE_PATH, -pmp PRED_MODULE_PATH
                         path of the prediction module
  --input_dir INPUT_DIR, -in INPUT_DIR
                         path of input directory
  --generate, -g        generate features from input signals
  --predict, -p         make predictions
  ```
  * The obtained time series, predictions, and visualization videos are stored in Demo/Outputs.
