# Detecting Location of a Person Real-time ( OpenCV / Python )


## Description

1. Aruco Markers have been used to Caliberate the Camera and find its focal Length.
2. Real-time Person Tracking is also perfomed using Aruco Markers, stuck on the peron.
3. The Program keeps track of the person's location for 30 frames even if their marker's detection is lost.
4. The Id's of Each Person corresponds to the Id's of the Aruco Markers.
5. Haar Cascade Classifiers are also added for Facial Recognition

## Installation
python version 3.7.3
Tested on MacOs (10.12)
``` sh
pip install -r requirements.txt
```
## Instructions to Run the program
1. Run CaliberateCamera.py and follow steps to Caliberate Camera and find its Focal Length.
    - Main.py will read the Focal Length from a text file
2. After Caliberation process is over, Run Main.py and pass the room coordinates to it.
    Example :
    Main.py --width 10 --height 10  --cam 5
    - It is Assumed that the camera's y position is 0. Which means it is always on a wall.
3. Every Person in the room need to carry an aruco marker for the detection.
4. The limitations and assumptions will be listed at the end of this readme. Details will be presented in the report.
5. Press Q to Exit.


### Caliberate the Camera
1. To Caliberate the Camera, you need the following
    - An ArucoMarker ( Preferrably of 4X4_250)
    - A Scale

2. Measure the ArucoWidth (AWiidth) and the distance from camera in cms and pass it to the CameraCaliberate.py
    -Example:
    CameraCaliberate.py --AWidth 9.1 --ADist 100
    - This means that from one corner to another corner its 9.1 cms and the distance of the marker from camera is 100 cms

3. A 3 second sleep is given to capture the right frame. Re-Run until you get a valid number printed on screen.
4. Once the Caliberation is Complete the focal length value is written to a Text file ***Focal.txt***
5. This focal length will be read by the Main Program.

Note:
    - This test case has ArucoWidth = 9.1 , ArucoDist = 100cms , frame.shape = (720,1280,3).

[Watch CameraCaliberate.py Video](https://www.dropbox.com/s/0jr54pl13oxz65q/VID-20200203-WA0002.mp4?dl=0)

In the video ,  my focal length is 881.6 .
I ran this a couple of times and took the average value as focal length which is 925.4287152275735



### Main Program

1. Test Case 1:
    - Camera at the middle of the wall
    - [Width = 10 ft , Depth = 10ft , Camera at 5ft] (https://www.dropbox.com/s/9jieoglyn7ggjme/10_10_5.mov?dl=0)

2. Test Case 2:
    - Camera near a corner of a room
    - [Width = 10 ft , Depth = 10ft , Camera at 2ft] (https://www.dropbox.com/s/z04tem6myu7fghq/10_10_2.mov?dl=0)
3. Docstrings are provided in the code.
4. Report.pdf will help you understand the methods, Datastructures used.

## RoadBlocks Faced / Experiments
### GENDER CLASSIFICATION:

1. Initially, Haar Cascade Classifiers were used for facial recognition.
    - ResNet model was used and "weights.hdf5" were obtained.

Approach :
1. Initial Approach was to use any one of
    - cv2.TrackerBoosting_create()
    - cv2.TrackerMIL_create()
    - cv2.TrackerKCF_create()
    - cv2.TrackerTLD_create()
    - cv2.TrackerMedianFlow_create()
    - cv2.TrackerGOTURN_create()
    - cv2.TrackerMOSSE_create()
    - cv2.TrackerCSRT_create()

2. Frame rate of my computer is 14 frames per second and hence, a Tracker was used to Track the Boxes Obtained from the classifiers.
3. Every 14th frame was sent to Gender Classifiers and the Trackers were updated.
4. The speed of the program slowed down very much and there was a huge lag.

A Gif from the Gender Classification Portion
<a href="https://imgflip.com/gif/3o11j0"><img src="https://i.imgflip.com/3o11j0.gif" title="made at imgflip.com"/></a>

### Centroid Tracking Algorithm

1. Centroid Tracking algorithm was experimented.
2. The Accuracy and speed were commendable but converting the boxes obtained on the screen to real world dimensions were tricky.
3. Computing the **Camera Parameters*** i.e(***Intrinsic, Extrinsic, Distorsion***) were a bit too costly and my system hung up often.
4. Other types of Camera Caliberations available online required multiple sensors and modules.


A Gif from the Centroid Tracking Portion
<a href="https://imgflip.com/gif/3o20fw"><img src="https://i.imgflip.com/3o20fw.gif" title="made at imgflip.com"/></a>


## LIMITATIONS AND ASSUMPTIONS
Assumption:
1. The Camera is always against one wall
2. The Camera is always perpendicular to the working space.
3. The Height does not matter as long as it can Track the Aruco Markers.

Limitation:
1. Lighting conditions may affect the detection of aruco Markers.
2. Without Aruco Markers, the progrom will not function
3. Two Arucomarkers of the same ID will result in an error and the program will malfunction
4. Too many Objects in the room can result in erraneous output
5. Tested with minimal number of ArucoMarkers.

System Details:
1. Tested on MacBook 2011
2. 8 GB Ram
3. MacOS Sierra

REFER REPORT.pdf for more details about the methods and data structures.
