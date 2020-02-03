import cv2
import PIL
import numpy as np
import os
from cv2 import aruco
import math
import imutils
import argparse
from main_functions import *


class Persons():
    def __init__(self, id, mod):
        self.x = 0
        self.y = 0
        self.id = id
        self.count = 0
        self.mod = mod

    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y + self.mod), 4,
                   (255, 255, 255), thickness=1, lineType=8, shift=0)
        cv2.putText(frame, "{}".format(self.id), (self.x, self.y + self.mod - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 1, cv2.LINE_AA)


def draw(human, frame_markers):
    for (x, y, w, h) in human:
        cv2.rectangle(frame_markers, (x, y), (x + w, y + h), (0, 0, 255), 3)


def Draw_map(room_map, room_x, room_y, Cam_x, mod):
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.rectangle(room_map, (20, 20),
                  (room_x - mod, room_y - mod), (255, 255, 255), 2)

    cv2.putText(room_map, 'Cam', (Cam_x, 13), font, 0.5,
                (255, 255, 255), 1, cv2.LINE_AA)


def find_dist(x1, x2, y1, y2):
    '''Finds Euclidean distance between the two points'''
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def Compute_Depth(focal, dist_pix, dist_real):
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


def Foot_to_cms(val):
    return int(30.48 * val)
