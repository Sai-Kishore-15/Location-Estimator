'''Camera Caliberation
This program Accepts the arucoMarker width in cms and its distance from the camera(cms) as arguments.
After computing the focal length it writes it to a text file.
This text file is later read by the main function

Theory:

Formula for depth
Dist_pix = width of the box in pixels
Dist_real = distance of the box in real world estimates
Depth = Known depth

Computing the focal length of the camera

F = (Dist_pix * Known depth) / Dist_real

Caliberation is complete, you can use this F to Compute every other depths
For example,
New Depth = (Dist_real * Focal)/ Dist_pix

-------------------------------------------------------------
Now To Caliberate the X axis.
Camera has 1280 pixels in my case. (i.e) 640 in the left and 640 in the right.

Depending upon the Camera position, The pixels are mapped to real_world units
For Example:
if Camera is placed at 2 ft and the wall's length is 10 ft.

The first 61 pixels ( 2 ft is 61 cms) is mapped to the first 640 pixels of the camera
The rest 305-61 pixels(10ft - 2ft ) is mapped to the other 640 pixels

Assuming that the Camera angle is perpendicular and the camera's Y axis is 0,
We Caliberate the X pixels to that of cms in the Screen

'''
import cv2
import numpy as np
import os
from cv2 import aruco
import math
import time
import imutils
import argparse
from caliberate_functions import *

# Global Variables
global camera_focal
global dist_real
camera_focal = None

# Starting Video Capture
cap = cv2.VideoCapture(0)
# Defining the parameters
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
# markerLength = 9.1   # Here, our measurement unit is centimetre.
arucoParams = cv2.aruco.DetectorParameters_create()

args = get_args()
dist_real = args.AWidth
known_depth = args.ADist

time.sleep(3)
while True:
    ret, frame = cap.read()
    # Converting to gray for ArucoMarkers()
    imgRemapped_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Corners of the AruCo Marker is Computed
    corners, ids, RejectedPoints = cv2.aruco.detectMarkers(
        imgRemapped_gray, aruco_dict, parameters=arucoParams)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    if np.all(ids != None):
        if camera_focal == None:
            dist_between_corner_pts = dist_real  # cms
            x1, y1 = (corners[0][0][0][0], corners[0][0][0][1])
            x2, y2 = (corners[0][0][1][0], corners[0][0][1][1])
            pixels_between_corner_pts = find_dist(x1, x2, y1, y2)
            camera_focal = Compute_Focal(
                pixels_between_corner_pts, known_depth, dist_real)

    cv2.imshow("ArucoMarkers", frame_markers)
    print(camera_focal)
    if camera_focal == None:
        print("Camera not caliberated")
        quit()

    with open("Focal.txt", "w+") as f:
        f.writelines([str(camera_focal) + "\n", str(dist_real) + "\n"])
    break

time.sleep(2)
cap.release()
cv2.destroyAllWindows()
