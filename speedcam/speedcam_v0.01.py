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

# from PollyReports import *
# from reportlab.pdfgen.canvas import Canvas

import home_lib as hlib
# import home_sendmail as hmail

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
#                          draw lines
#
# --------------------------------------------------------------------

def draw_lines(img, lines):
    try:

        for line in lines:
            coords = line[0]
            # print(coords)
            cv2.line(img, (coords[0], coords[1]),
                          (coords[2], coords[3]),
                          [255,255,255],     # colour
                          3)                 # thickness
    except:
        pass

# --------------------------------------------------------------------
#
#                          process
#
# --------------------------------------------------------------------




def process_img(orig_img):
    processed_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
    # processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)
    vertices = np.array([[0, 300], [800, 250], [800, 500], [0,600]], np.int32)

    # Calc range of colours
    # (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(processed_img)
    # print('min {} max {}'.format(minVal, maxVal))

    processed_img  = roi(processed_img, [vertices])

    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180,np.array([]), 20, 15)
    draw_lines( processed_img, lines)
    return(processed_img)

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

    while (True):
        screen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
        new_screen = process_img(screen)
#        printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8')

        print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()

        cv2.imshow('window',new_screen)
        # cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    retval = hlib.SUCCESS

    print('Done...')

    return retval

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    l_retval = main()
    if l_retval == hlib.SUCCESS:
        exit
    else:
        exit(l_retval)

# --- eof ---
