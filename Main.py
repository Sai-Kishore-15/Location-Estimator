''' Real Time Location Detector using ArucoMarkers
1. Accepts --Width ( Width of the room in ft ) , -- breadth ( Breadth of the room in ft ), --cam ( Camera Distance of the room in ft )
2. Displays the location of the person in the room on a room Map.

Uses Aruco Markers for the detection hence assumes
1) every person has an aruco marker attached to them
2) All the people have different ArucoMarker Ids
'''

import cv2
import PIL
import numpy as np
import os
from cv2 import aruco
import math
import imutils
import argparse
from main_functions import *
global camera_focal
global unwanted
global Adder
global mod

# variables
face_size = 64
Adder = 40
Counter_Threshold = 30
camera_focal = None
unwanted = []

human_cascade = cv2.CascadeClassifier("haarcascade_facedefault.xml")

# Importing Focal Length and Markerlength from Caliberation data
with open("Focal.txt", "r") as f:
    camera_focal = (f.readline())
    dist_real = (f.readline())
    if camera_focal == '':
        print("Camera Not Caliberated")
        quit()
    else:
        camera_focal.strip("\n")
        dist_real.strip("\n")
        print("Dist", dist_real)
        camera_focal, dist_real = float(camera_focal), float(dist_real)

# Starting Video Capture
cap = cv2.VideoCapture(0)
# Defining the parameters
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters_create()

# Room Dimensions
args = get_args()
room_x = Foot_to_cms(args.width) + Adder
room_y = Foot_to_cms(args.breadth) + Adder
Camera_x = Foot_to_cms(args.cam)

Offset = room_x / Camera_x
X_mod = 2 - Offset
X_mod = Foot_to_cms(X_mod)
mod = (Adder // 2)

# This Dictionary stores " ID's : Object(ID) "
Obj_Dict = {}

while True:
    # reading frames
    ret, frame = cap.read()
    room_map = np.zeros((room_y, room_x, 3), dtype="uint8")

    # Draws the map
    Draw_map(room_map, room_x, room_y, Camera_x, mod)
    human = human_cascade.detectMultiScale(
        frame, 1.1, 6, minSize=(face_size, face_size))

    # Converting to gray for ArucoMarkers()
    imgRemapped_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, RejectedPoints = cv2.aruco.detectMarkers(
        imgRemapped_gray, aruco_dict, parameters=arucoParams)

    # Draws ArucoMarkers and Face
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    draw(human, frame_markers)

    # Functionality
    # Shows the disappeared Objects for 30 frames and then deletes it
    # Special case when ids is none but len(Objects) isnt. Counter starts for all objects
    if np.all(ids == None) and len(Obj_Dict) != 0:
        for i in Obj_Dict:
            Obj_Dict[i].count += 1

        if Obj_Dict[i].count >= Counter_Threshold:
            unwanted.append(i)
        if len(unwanted) > 0:
            del Obj_Dict[unwanted[0]]
            unwanted = unwanted[1:]

    # Similar Case but counter only deletes elements which arent present in idlist.
    for i in Obj_Dict:
        if id_list:
            if i not in id_list:
                Obj_Dict[i].count += 1
        Obj_Dict[i].draw(room_map)
        if Obj_Dict[i].count >= Counter_Threshold:
            unwanted.append(i)
    if len(unwanted) > 0:
        del Obj_Dict[unwanted[0]]
        unwanted = unwanted[1:]

    # Detection and Object Creation
    if np.all(ids != None):
        id_list = [i[0] for i in ids]
        for i in id_list:
            if i in Obj_Dict.keys():
                Obj_Dict[i].count = 0
                continue
            else:
                Obj_Dict[i] = Persons(i, mod)

        for i in range(len(corners)):

            x1, y1 = (corners[i][0][0][0], corners[i][0][0][1])
            x2, y2 = (corners[i][0][1][0], corners[i][0][1][1])
            x3, y3 = (corners[i][0][2][0], corners[i][0][2][1])
            x4, y4 = (corners[i][0][3][0], corners[i][0][3][1])

            centroid_x = (corners[i][0][0][0] + corners[i][0][1]
                          [0] + corners[i][0][2][0] + corners[i][0][3][0]) // 4
            pixels_between_corner_pts = find_dist(x1, x2, y1, y2)
            real_depth = int(Compute_Depth(
                camera_focal, pixels_between_corner_pts, dist_real))

            '''Once Real Depth is found (refer CameraCaliberate.py for theory), we caliberte x
                The screen os divided into half,
                One Half Corresponds to the left side of the map and the other to the right.
                With linear interpolation , the ratios of pixel movement in each direction is computed'''

            room_actual_x = room_x - Adder
            splits = room_actual_x - Camera_x
            Half_frame = frame.shape[1] // 2

            if centroid_x >= Half_frame:
                room_pos_x = (Camera_x / Half_frame) * \
                    (frame.shape[1] - centroid_x)
                room_pos_x = int(room_pos_x)

            else:
                room_pos_x = (splits / Half_frame) * centroid_x
                room_pos_x = int(room_actual_x - room_pos_x)
            # We have drawn a rectangle in the window to indicate the size of the room
            # Thus we have to add an offset to cover the extra space.
            room_pos_x += mod
            try:
                Obj_Dict[ids[i][0]].x = room_pos_x
                Obj_Dict[ids[i][0]].y = real_depth
            except:
                pass

    cv2.imshow("ArucoMarkers", frame_markers)
    cv2.imshow("Room Map ", room_map)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
