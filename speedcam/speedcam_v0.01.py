"""
Validate spreadsheet data is same as db data

"""

# pip install opencv-python

# Readings:
#    https://www.youtube.com/watch?v=ks4MPfMq8aQ       # youtube on GTA5
#    https://pypi.python.org/pypi/opencv-python         # opencv



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

# from email.mime.text import MIMEText
import argparse

import numpy as np
from PIL import ImageGrab
import cv2

# from PollyReports import *
# from reportlab.pdfgen.canvas import Canvas

import home_lib as hlib
import home_sendmail as hmail


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
    # Fetch program arguments

    # -------------------------------------
    # Fetch config
    # https://stackoverflow.com/questions/24129253/screen-capture-with-opencv-and-python-2-7

    while (True):
        printscreen_pil =  ImageGrab.grab()
        printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8').reshape(
                                  (printscreen_pil.size[1],printscreen_pil.size[0],3))
        cv2.imshow('window',printscreen_numpy)
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
