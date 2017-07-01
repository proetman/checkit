"""
Validate spreadsheet data is same as db data

"""

# pip install opencv-python

# Readings:
#    https://www.youtube.com/watch?v=ks4MPfMq8aQ       # youtube on GTA5
#    https://pypi.python.org/pypi/opencv-python         # opencv
#    http://morefunscience.blogspot.com.au/2012/05/calculating-speed-using-webcam.html

# Image and video analysis (tutorial.l)
#    https://pythonprogramming.net/loading-images-python-opencv-tutorial/



from __future__ import division
from __future__ import print_function

# import datetime
# import re
# import textwrap

# import numpy as np
# import pandas as pd

# import webbrowser
# import bs4
# import requests
# import email
# import smtplib

import time

# from email.mime.text import MIMEText
import argparse

import numpy as np
from PIL import ImageGrab
import cv2
import matplotlib.pyplot as plt
# from PollyReports import *
# from reportlab.pdfgen.canvas import Canvas

import home_lib as hlib
# import home_sendmail as hmail

# --------------------------------------------------------------------
#
#                          Globals
#
# --------------------------------------------------------------------

KERNEL = np.ones((6,6), np.uint8)
MOVEMENT_THRESHOLD = 1000000

# --- image processing
# --------------------------------------------------------------------
#
#                          region of interest
#
# --------------------------------------------------------------------

def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

# --------------------------------------------------------------------
#
#                          process_img
#
# --------------------------------------------------------------------
def process_img(orig_img):
    processed_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
    # processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    processed_img = cv2.Canny(processed_img, threshold1=100, threshold2=200)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(processed_img)
    # print('min {} max {}'.format(minVal, maxVal))
    return(processed_img)


# --------------------------------------------------------------------
#
#                          plot graph
#
# --------------------------------------------------------------------
#

def plot_result(x, y):
    plt.plot(x, y)

    plt.xlabel('Movement')
    plt.ylabel('Frames')
    plt.grid(True)
    plt.savefig("test.png")
    plt.show()

# --------------------------------------------------------------------
#
#                          Get Motion Detection
#
# --------------------------------------------------------------------
#
#  at the beginning of a car
#    curr - 2 has nothing
#    curr - 1 has nothing
#    curr     has car edge

def _get_motion_detection_frame(curr_min2, curr_min1, frame):
        d1 = cv2.absdiff(frame, curr_min1)
        d2 = cv2.absdiff(curr_min1, curr_min2)
        motion_detection_frame = cv2.bitwise_xor(d1, d2)

        # cv2.imshow('frame', frame)
        # cv2.imshow('curr_min1', curr_min1)
        # cv2.imshow('curr_min2', curr_min2)
        # cv2.imshow('d1', d1)
        # cv2.imshow('d2', d2)

        # time.sleep(1)
        # Remove any single white dots (background movements)
        motion_detection_frame  = cv2.erode(motion_detection_frame, KERNEL, iterations = 1)
        #  motion_detection_frame  = cv2.dilate(motion_detection_frame, KERNEL, iterations = 1)
        return motion_detection_frame

# --------------------------------------------------------------------
#
#                          Process
#
# --------------------------------------------------------------------


def process(p_file):

    cap = cv2.VideoCapture(p_file)
    count = 0
    curr_min1 = None
    curr_min2 = None

#    x = []
#    y = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        have_car = False
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if curr_min2 is not None:
            motion_detection_frame = _get_motion_detection_frame(curr_min2,  curr_min1, grey)

            ret, mask = cv2.threshold(motion_detection_frame, 5, 255, cv2.THRESH_BINARY_INV)
            im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            processed_img = cv2.Canny(im2, threshold1=200, threshold2=300)
            # processed_img  = cv2.erode(processed_img, KERNEL, iterations = 1)
            # processed_img  = cv2.dilate(processed_img, KERNEL, iterations = 1)
            p_im2, p_contours, p_hierarchy = cv2.findContours(processed_img,
                                                              cv2.RETR_LIST,
                                                              cv2.CHAIN_APPROX_SIMPLE)


            sum_pix = np.sum(motion_detection_frame)
#            x.append(count)
#            y.append(sum_pix)

            height, width = motion_detection_frame.shape
            min_x, min_y = width, height
            max_x = max_y = 0

            cv2.drawContours(frame, p_contours, -1, (0,0,255), 3)

            c_count = 0
            for contour in p_contours:
                c_count += 1
                (x,y,w,h) = cv2.boundingRect(contour)
                # print('x = {}; min max = {},{}'.format(x,min_x, max_x))
                min_x, max_x = min(x, min_x), max(x+w, max_x)
                min_y, max_y = min(y, min_y), max(y+h, max_y)
#                if w > 80 and h > 80:
#                    cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)

            print('processed {} contours'.format(c_count))
            if max_x - min_x > 0 and max_y - min_y > 0:
                cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

            cv2.imshow('window-name', frame)
            cv2.imshow('im2', processed_img)


            if (sum_pix > MOVEMENT_THRESHOLD):
                have_car = True


            print("count = {} car{} sum pix {:,d}".format(count, have_car, sum_pix))





        # grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('window-name', grey)
        # cv2.imwrite('c:/temp/frames/frame_{}.jpg'.format(count), frame)    #  process_img(frame))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        curr_min2 = curr_min1
        curr_min1 = grey



    cap.release()
    cv2.destroyAllWindows()

#    plot_result(x,y)

    return hlib.SUCCESS


#            hsv = cv2.cvtColor(motion_detection_frame, cv2.COLOR_BGR2HSV)
#            min_color = np.array([10,0,0])
#            max_color = np.array([255,255,255])
#            car_mask = cv2.inRange(hsv, min_color, max_color)
#            res = cv2.bitwise_and(motion_detection_frame, motion_detection_frame, mask=car_mask)
# --- Program Init
# --------------------------------------------------------------------
#
#                          initialise
#
# --------------------------------------------------------------------


def initialise(p_filename=None):
    """
    Necessary initialisations for command line arguments
    """
    # Logfile for logging
    log_filename = hlib.log_filename_init(p_filename)
    if log_filename is None:
        print("\nError: Failed to initialise Log File Name. aborting\n")
        return hlib.FAIL_GENERIC

    parser = argparse.ArgumentParser(description="""
     Example command lines:

    Run on local machine:
    -d DEBUG  -t table -f file.xlsx --target_conn localhost

    Run on Terminal Server:
    -d DEBUG -t table -f file.xlsx  --target_db instance.user@host:db (this may change)
    -d DEBUG -t table -f file.csv   --target_db instance.user@host:db (this may change)

    --target_db localhost
    --short_code "unit agency restriction"

          """, formatter_class=argparse.RawTextHelpFormatter)
    # Add debug arguments
    parser.add_argument('-f', '--file',
                        help='file to process',
                        required=True)

    # Add debug arguments
    parser.add_argument('-d', '--debug',
                        help='Log messages verbosity: NONE (least), DEBUG (most)',
                        choices=('NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'),
                        default="INFO",
                        required=False)

    # Sort though the arguments, ensure mandatory are populated
    args = hlib.args_validate(parser, log_filename)

    return (args, log_filename)

# --------------------------------------------------------------------
#
#                          main
#
# --------------------------------------------------------------------


def main():
    """
    This program tests that data in CSV file matches data in a table.
    """

    args, dummy_l_log_filename_s = initialise()

    # -- Initialise
    if not hlib.init_app(args):
        print('Failed to init app, aborting')
        return hlib.FAIL_GENERIC

    # -------------------------------------
    # Fetch program argumentsq
    # -------------------------------------
    # Fetch config
    # https://stackoverflow.com/questions/24129253/screen-capture-with-opencv-and-python-2-7

    last_time = time.time()

    retval = process(args['file'])

    print('Done...')

    return retval

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    l_retval = main()
    print('the end')
    if l_retval == hlib.SUCCESS:
        exit
    else:
        exit(l_retval)

# --- eof ---
