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
import PIL
import numpy as np
import os
from cv2 import aruco
import math
import imutils
import argparse


face_size = 64

global camera_focal
global unwanted
global Adder
global mod
human_cascade = cv2.CascadeClassifier("haarcascade_facedefault.xml")
human_cascade_lower = cv2.CascadeClassifier(" ")
unwanted = []

with open("Focal.txt", "r") as f:
    camera_focal = float(f.read())


def draw(human):
    for (x, y, w, h) in human:
        cv2.rectangle(frame_markers, (x, y), (x + w, y + h), (0, 0, 255), 3)


def Draw_map(room_map, room_x, room_y, Cam_x):
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.rectangle(room_map, (20, 20),
                  (room_x - mod, room_y - mod), (255, 255, 255), 2)

    cv2.putText(room_map, 'Cam', (Cam_x, 13), font, 0.5,
                (255, 255, 255), 1, cv2.LINE_AA)


class Persons():
    global X_mod

    def __init__(self, id):
        self.x = 0
        self.y = 0
        self.id = id
        self.count = 0

    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y + 20), 4,
                   (255, 255, 255), thickness=1, lineType=8, shift=0)
        cv2.putText(frame, "{}".format(self.id), (self.x, self.y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 1, cv2.LINE_AA)


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
    dist_real = 9.1  # cms
    known_depth = 100  # cms
    Focal = (dist_pix * known_depth) / dist_real
    return Focal


def Compute_Depth(focal, dist_pix):
    dist_real = 9.1  # cms
    return (dist_real * focal) / dist_pix


def get_args():
    parser = argparse.ArgumentParser(description="This script detects faces from web cam input, "
                                                 "and estimates age and gender for the detected faces.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--width", type=int, required=True,
                        help="width the room ")
    parser.add_argument("--breadth", type=int, required=True,
                        help="depth of the room")

    parser.add_argument("--cam", type=int, default=5,
                        help="width of the camera")

    args = parser.parse_args()
    return args



# Starting Video Capture
cap = cv2.VideoCapture(0)
# Defining the parameters
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
markerLength = 9.1   # Here, our measurement unit is centimetre.
arucoParams = cv2.aruco.DetectorParameters_create()

# Room Dimensions


def Foot_to_cms(val):
    return int(30.48 * val)


args = get_args()
Adder = 40
room_x = Foot_to_cms(args.width) + Adder
room_y = Foot_to_cms(args.breadth) + Adder
Camera_x = Foot_to_cms(args.cam)

Offset = room_x / Camera_x
X_mod = 2 - Offset
X_mod = Foot_to_cms(X_mod)
mod = (Adder // 2)


# room_x = 305 + 40
# room_y = 305 + 40
# Camera_x = 305 // 2
Obj_Dict = {}

while True:
    ret, frame = cap.read()
    # frame = imutils.resize(frame, width=640)
    room_map = np.zeros((room_y, room_x, 3), dtype="uint8")
    Draw_map(room_map, room_x, room_y, Camera_x)
    human = human_cascade.detectMultiScale(
        frame, 1.1, 6, minSize=(face_size, face_size))

    # Converting to gray for ArucoMarkers()
    imgRemapped_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("video",imgRemapped_gray)
    corners, ids, RejectedPoints = cv2.aruco.detectMarkers(
        imgRemapped_gray, aruco_dict, parameters=arucoParams)

    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    draw(human)

    if np.all(ids == None) and len(Obj_Dict) != 0:
        for i in Obj_Dict:
            Obj_Dict[i].count += 1

        if Obj_Dict[i].count >= 30:
            unwanted.append(i)
        if len(unwanted) > 0:
            del Obj_Dict[unwanted[0]]
            unwanted = unwanted[1:]

    for i in Obj_Dict:
        if id_list:
            if i not in id_list:
                Obj_Dict[i].count += 1
        Obj_Dict[i].draw(room_map)
        if Obj_Dict[i].count >= 30:
            unwanted.append(i)

    if len(unwanted) > 0:
        del Obj_Dict[unwanted[0]]
        unwanted = unwanted[1:]

    if np.all(ids != None):
        id_list = [i[0] for i in ids]

        for i in id_list:
            if i in Obj_Dict.keys():
                Obj_Dict[i].count = 0
                continue
            else:
                Obj_Dict[i] = Persons(i)

        if camera_focal == None:
            dist_between_corner_pts = 9.1  # cms
            x1, y1 = (corners[0][0][0][0], corners[0][0][0][1])
            x2, y2 = (corners[0][0][1][0], corners[0][0][1][1])
            pixels_between_corner_pts = find_dist(x1, x2, y1, y2)
            camera_focal = Compute_Focal(pixels_between_corner_pts)

        for i in range(len(corners)):

            dist_between_corner_pts = 9.1  # cms
            x1, y1 = (corners[i][0][0][0], corners[i][0][0][1])
            x2, y2 = (corners[i][0][1][0], corners[i][0][1][1])
            x3, y3 = (corners[i][0][2][0], corners[i][0][2][1])
            x4, y4 = (corners[i][0][3][0], corners[i][0][3][1])

            centroid_x = (corners[i][0][0][0] + corners[i][0][1]
                          [0] + corners[i][0][2][0] + corners[i][0][3][0]) // 4
            pixels_between_corner_pts = find_dist(x1, x2, y1, y2)
            real_depth = int(Compute_Depth(
                camera_focal, pixels_between_corner_pts))

            room_actual_x = room_x - Adder
            splits = room_actual_x - Camera_x
            Half_frame = frame.shape[1] // 2

            if centroid_x >= Half_frame:
                room_pos_x = (Camera_x / Half_frame) * \
                    (frame.shape[1] - centroid_x)
                room_pos_x = int(room_pos_x)

                # room_pos_x = room_pos_x - splits
            else:
                room_pos_x = (splits / Half_frame) * centroid_x
            # room_pos_x = (room_actual_x / frame.shape[1]) * centroid_x

                room_pos_x = int(room_actual_x - room_pos_x)
            room_pos_x += mod
            try:
                Obj_Dict[ids[i][0]].x = room_pos_x
                Obj_Dict[ids[i][0]].y = real_depth
            except:
                pass
            # Obj_Dict[ids[i][0]].draw(room_map)

    cv2.imshow("ArucoMarkers", frame_markers)
    cv2.imshow("Room Map ", room_map)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
