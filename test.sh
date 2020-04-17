# Generate time series
#python src/generate_time_series.py -rg 1 2 3 4 5 6 -pmp PredictionModule -in Demo -ofp ../../OpenFace


# Make predictions
python src/predict.py -rg 1 2 3 4 5 6 -pmp PredictionModule -in Demo -t h


# Generate time series video from the obtained predictions
python src/animation.py -in Demo


# using visbrain to visulize the predictions of the ROIs
python src/visualization.py -in Demo
