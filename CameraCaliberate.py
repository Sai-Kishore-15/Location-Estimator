'''Real time Aruco Edge Detection'''

''' Formula for depth
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
1) We know the opposite Wall's length.
2) We know the pixel length of the wall.

Assuming that the camera angle and orientation does not change.
WallPix = number of pixels from one edge of the wall to other.
WallDist = The World distanace ( cm or inches or foot)

Note: WallDist must be same as Dist_real used to compute Depth
Calib_Ratio = (WallDist / WallPix)
World_X = (Current_Xpixel_value) * Calib Ratio.
'''
import cv2
import numpy as np
import os
from cv2 import aruco
import math
import time
import imutils
import argparse

global camera_focal
global dist_real
# camera_focal = 925.4287152275735
camera_focal = None


def find_dist(x1, x2, y1, y2):
    '''Finds Euclidean distance between the two points'''
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def Dist_text(focal, frame, coord):
    '''Prints the value of the distance on the screen'''

    text = 'Depth {} '.format(focal)
    cv2.putText(frame, text, coord, cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2, cv2.LINE_AA)


def Compute_Focal(distPix):
    dist_pix = distPix
    # dist_real = 9.1  # cms
    # known_depth = 100  # cms
    Focal = (dist_pix * known_depth) / dist_real
    return Focal


def Compute_Depth(focal, dist_pix):
    # dist_real = 9.1  # cms
    return (dist_real * focal) / dist_pix


def get_args():
    parser = argparse.ArgumentParser(description="This script detects faces from web cam input, "
                                                 "and estimates age and gender for the detected faces.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--AWidth", type=float, required=True,
                        help="width the ArucoMarker in cms ")

    parser.add_argument("--ADist", type=int, required=True,
                        help="width the ArucoMarker in cms ")

    args = parser.parse_args()
    return args


# Starting Video Capture
cap = cv2.VideoCapture(0)
# Defining the parameters
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
# markerLength = 9.1   # Here, our measurement unit is centimetre.
arucoParams = cv2.aruco.DetectorParameters_create()


def Foot_to_cms(val):
    return int(30.48 * val)


args = get_args()
dist_real = args.AWidth
known_depth = args.ADist

time.sleep(3)
while True:
    ret, frame = cap.read()
    # frame = imutils.resize(frame, width=640)
    # Converting to gray for ArucoMarkers()
    imgRemapped_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("video",imgRemapped_gray)
    corners, ids, RejectedPoints = cv2.aruco.detectMarkers(
        imgRemapped_gray, aruco_dict, parameters=arucoParams)

    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    if np.all(ids != None):
        if camera_focal == None:
            dist_between_corner_pts = dist_real  # cms
            x1, y1 = (corners[0][0][0][0], corners[0][0][0][1])
            x2, y2 = (corners[0][0][1][0], corners[0][0][1][1])
            pixels_between_corner_pts = find_dist(x1, x2, y1, y2)
            camera_focal = Compute_Focal(pixels_between_corner_pts)

    cv2.imshow("ArucoMarkers", frame_markers)
    print(camera_focal)

    with open("Focal.txt", "w+") as f:
        f.write(str(camera_focal))
    break

time.sleep(2)
cap.release()
cv2.destroyAllWindows()
