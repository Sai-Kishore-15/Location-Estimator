import cv2
import numpy as np
import math
import time
import imutils
import argparse


def Foot_to_cms(val):
    return int(30.48 * val)


def find_dist(x1, x2, y1, y2):
    '''Finds Euclidean distance between the two points'''
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def Dist_text(focal, frame, coord):
    '''Prints the value of the distance on the screen'''

    text = 'Depth {} '.format(focal)
    cv2.putText(frame, text, coord, cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2, cv2.LINE_AA)


def Compute_Focal(distPix, known_depth, dist_real):
    ''' Params : distPix ( the Pixel distance of an edge in the aruco)
        returns: Focal Length'''
    dist_pix = distPix
    Focal = (dist_pix * known_depth) / dist_real
    return Focal


def Compute_Depth(focal, dist_pix, dist_real):
    ''' Once Focal Length is computed, This formula is used to compute Depth in Cms'''
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
