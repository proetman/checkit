"""
Validate spreadsheet data is same as db data

"""
from __future__ import division
from __future__ import print_function

import argparse
# import datetime
# import re
# import textwrap

# import numpy as np
# import pandas as pd

# import webbrowser
import bs4
import requests
from selenium import webdriver

import home_lib as hlib


# --------------------------------------------------------------------
#
#             Global /  Constants
#
# --------------------------------------------------------------------


# --- process
# --------------------------------------------------------------------
#
#                          setup load details
#
# --------------------------------------------------------------------


def process():
    """
    run a process
    """
    print('Start process')

    browser = webdriver.Firefox()

    # res = requests.get('https://www.service.transport.qld.gov.au/checkrego/application/VehicleSearch.xhtml?windowId=e85')
    res = requests.get('https://www.service.transport.qld.gov.au/checkrego/application/TermAndConditions.xhtml?windowId=3ab')
    res.raise_for_status()
    noStarchSoup = bs4.BeautifulSoup(res.text, "lxml")
    type(noStarchSoup)
    return


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
        return hlib.FAIL_GENERIC

    # -------------------------------------
    # Fetch program arguments

    # p_debug_type = args['debug_type']
    process()
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
