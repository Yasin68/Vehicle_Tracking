python3 util.py -p $1 && \
python3 getLaneCoordinates.py && \
python3 makeVideo.py && \
rm data/slope_intercept.txt data/tracking_vehicle.json && \
rm -r data/frame data/final
