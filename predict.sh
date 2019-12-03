# Generate time series
python src/predict.py -rg 1 2 3 4 5 6 -t r  -ofp ../../OpenFace -pmp PredictionModule -in Demo -g
# Make predictions
python src/predict.py -rg 1 2 3 4 5 6 -t r  -ofp ../../OpenFace -pmp PredictionModule -in Demo -p
# Generate time series video from the obtained predictions
python src/animation.py -in Demo
# using visbrain to visulize the prediction in the brain
python src/visualization.py -in Demo
