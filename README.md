A tool for predicting and visualizing the fMRI brain activity during bidirectional conversations of type human-human or human-machine. The current version of the executable of the interface "BrainPredict" is compiled in Linux, nevertheless, the code source is provided on Qt with C++17 for compilation on other systems. While the prediction module is implemented in Python3, and can be executed from terminal or using the interface. The conversation's language required by the current version are only french and english.

__This project is still in development__. It is done  during my postdoctoral research supervised by Laurent Prévot and Magalie Ochs, in the context of the PhysSocial project https://amidex.hypotheses.org/2051 proposed by Thierry Chaminade, where the training data are collected from a fRMI experiment conducted on 24 participants.


## Requirements
  * Python>=3.6
  * Openface  (https://github.com/TadasBaltrusaitis/OpenFace) is required to compute facial features from videos.
  * SPPAS (http://www.sppas.org/) is required for automatic annotation and segmentation of the speech (a copy is included in the code source of the prediction module).
  * The FFmpeg multimedia framework:
    ```bash
      sudo apt-get install ffmpeg
    ```
  * Python packages:
    ```bash
      pip install -r requirements.txt
    ```
  * Spacy  models:
    ```bash
        python -m spacy download fr_core_news_sm
        python -m spacy download en_core_web_sm
    ```

## Demo: using Qt Creator Interface
The working directory must be specified and must contain an Inputs folder containing speech, eyetracking, and video folders.
First, install the following requirements:

```bash
  sudo apt-get install qtmultimedia5-dev libqt5multimediawidgets5
    libqt5multimedia5-plugins libqt5multimedia5
 ```
Then run the executable after setting the execution rights:

  ```bash
    chmod +x BrainPredict
    sh BrainPredict sh
  ```

## Demo: using the command line
  * To run a demo, we need a video file (of the interlocutor), and the audios of both the participant and the interlocutor, and an eyetracking file of the participant.

  * A example is provided in the folder "Demo". To run the example:

  ```bash
 # Generate time series
 python src/generate_time_series.py -rg 3 10 21 -pmp PredictionModule -in Demo -ofp 'openface path'

 # Make predictions
 python src/predict.py -rg 3 10 21 -pmp PredictionModule -in Demo -t r

 # Generate time series video from the obtained predictions
 python src/animation.py -in Demo

 # Using visbrain to visualize the prediction in the brain
 python src/visualization.py -in Demo
  ```
   * The required arguments:
   ```bash
  --regions REGIONS [REGIONS ...], -rg REGIONS [REGIONS ...]
                        Numbers of brain areas to predict (see
                        brain_areas.tsv)
  --type TYPE, -t TYPE  conversation type (human or robot)

  --pred_module_path PRED_MODULE_PATH, -pmp PRED_MODULE_PATH
                        path of the prediction module
  --openface_path OPENFACE_PATH, -ofp OPENFACE_PATH
                        path of Openface
  --input_dir INPUT_DIR, -in INPUT_DIR
                        path of input directory
  ```
