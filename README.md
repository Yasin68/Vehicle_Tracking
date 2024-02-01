# Vehicle_Tracking

<img src="data/test.gif" width="1080" height="720"/>

This project tracks cars (the car and the lane it is in) using object detection model RCNN and a basic tracking algorithm that determines the class label for the object for which the distance between detected objects is less than a threshold and computes the distance between detected objects between each frame. The camera on top of a bridge, watching traffic, provides the perspective for the video.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

1. ``` python3 util.py -p (path to video)``` (this will convert the video to frames and save them in the frames folder)
2. ``` python3 getLaneCoordinates.py ``` (a new window will open. Label lanes from left to right lane by clicking on the image. Press 's' to save the coordinates)
3. ``` python3 getLaneCoordinates.py -t ``` ([Optional] click on the lane to test the coordinates you have saved)
4. ``` python3 getDistance.py ``` ([Optional] this will label the vehicles using a simple tracking algorithm and save the labeled vehicle in data folder if you want to see labels)
5. ``` python3 makeVideo.py ``` (this assumes, that you have cordinates of detected vehicle for each frame in a json file in data folder. Please check data folder for ''if all goes well this will get the final output video and final tracking_vehicle.json file is saved)

## Methodology
1. Use RCNN to detect vehicles, and save the bounding box coordinates for each frame in a JSON file. The Jupyter notebook that is provided is used for this.
2. Use getLaneCoordinates.py to draw lines on the image to represent the lanes. Slope and intercept are saved for lane lines in a file. To test the script, pass the -t flag.
3. Using getDistance.py, determine the distance between the objects that have been detected, assign labels appropriately, and determine which lane they are in.
4. The makeVideo.py script transforms each frame from the source video into a labelled frame that includes the car and lane numbers. saves the final JSON file containing the bounding box coordinates, label, car number, and lane information for every frame.
## Improvements
1.Make use of the better tracking algorithm.
Currently, only car detections are tracked for videos featuring multiple vehicles.
At the moment, the algorithm gives the same label to objects whose distance between two consecutive frames is both minimum and less than a threshold. This method may have a drawback in that the object may not be tracked by the system if a detection is missed in between frames. The same holds true for items that are momentarily obscured. Thus, in order to obtain a more accurate estimate of the object's position, we must find a way to average data from several frames.

2. Rather than drawing lanes by hand, use image processing to identify them.

3. Have the script execute in real time rather than analysing the entire video at once.


