"""
Validate spreadsheet data is same as db data

"""
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
import pickle
import time
from selenium import webdriver
from datetime import datetime

# from PollyReports import *
# from reportlab.pdfgen.canvas import Canvas

import home_lib as hlib
import home_sendmail as hmail


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
def generate_report(p_all_info):
    """ Generate html report """
    """ hmmmm, will do the html stuff later. Bigger fish to fry now!"""

    rep_format = "{:15s} {:15s} {:45s} {}\r\n"

    output_data = rep_format.format('Rego', 'Date', 'Descripion', 'Days to go')
    output_data += rep_format.format('-'*15, '-'*15, '-'*45, '-'*45)

    for row in p_all_info:
        curr_rego = ''
        curr_date = ''
        curr_desc = ''

        for key, val in row.items():
            print('key = {}, val ={}'.format(key, val))
            if key == 'Description':
                curr_desc = val
            if key == 'Registration number':
                curr_rego = val
            if key == 'Expiry':
                curr_date = val

        actual_date = datetime.strptime(curr_date,'%d/%m/%Y')
        today = datetime.now()
        date_diff = actual_date - today

        output_data += rep_format.format(curr_rego, curr_date, curr_desc, date_diff)

    return output_data
    # rpt = Report
# --------------------------------------------------------------------
#
#                          process
#
# --------------------------------------------------------------------


def process(p_rego_plates):
    """
    run a process
    """
    print('Start process')

    all_vehicles = []

    for vehicle in p_rego_plates:

        dot_info = fetch_plate_info(vehicle)
        all_vehicles.append(dot_info)

    return all_vehicles
    # Send the message via our own SMTP server.
#    s = smtplib.SMTP('smtp.gmail.com')
#    s.send_message(msg)
#    s.quit()

# --------------------------------------------------------------------
#
#                          Fetch plate info
#
# --------------------------------------------------------------------


def fetch_plate_info(p_vehicle):
    """
    run a process
    """

    veh_plate = p_vehicle[0]
    veh_email = p_vehicle[1]
    veh_desc = p_vehicle[2]

    browser = webdriver.Firefox()
    browser.get('https://www.service.transport.qld.gov.au/checkrego/application/TermAndConditions.xhtml?windowId=3ab')
    conf_button = browser.find_element_by_name('tAndCForm:confirmButton')
    conf_button.click()
    time.sleep(1)
    reg_field = browser.find_element_by_id('vehicleSearchForm:plateNumber')
    reg_field.send_keys(veh_plate)

    time.sleep(0.5)
    conf_button = browser.find_element_by_name('vehicleSearchForm:confirmButton')
    conf_button.click()

    time.sleep(1)

    dot_info = {}

    dot_info['orig_rego'] = veh_plate
    dot_info['email'] = veh_email
    dot_info['veh_desc'] = veh_desc

    for row in browser.find_elements_by_css_selector("dl.data"):
        cell_names = row.find_elements_by_tag_name('dt')
        cell_data = row.find_elements_by_tag_name('dd')
        cell_counter = 0
        for c in cell_names:
            dot_info[c.text] = cell_data[cell_counter].text
            cell_counter += 1

    browser.quit()

    return dot_info
# --- save data
# --------------------------------------------------------------------
#
#                          save data
#
# --------------------------------------------------------------------


def save_data(p_all_info):
    """
    save all data to a csv file, and pickle file
    """
    pickle_file = '{}/{}'.format(hlib.SAVE_DIR, 'dept_of_transport.pickle')

    with open(pickle_file, 'w') as pfile:
        pickle.dump(p_all_info, pfile)

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

    # send_email(email_config)

    # -------------------------------------
    # Fetch program arguments

    # -------------------------------------
    # Fetch config

    rego_plates = hlib.fetch_rego_plates()

    # p_debug_type = args['debug_type']
    all_info = process(rego_plates)

#    if not save_data(all_info):
#        return(hlib.FAIL_GENERIC)

    text_report = generate_report(all_info)

    rep_file = '{}/{}'.format(hlib.SAVE_DIR, 'dept_of_transport_report.txt')
    file = open(rep_file, 'w')
    file.write(text_report)
    file.close()

#    if not save_report(all_info):
#        return(hlib.FAIL_GENERIC)

    hmail.send_email('proetman@gmail.com',
                     p_subject='Weekly Rego Report',
                     p_inline=rep_file)

    hmail.send_email('annieroetman@gmail.com',
                     p_subject='Weekly Rego Report',
                     p_inline=rep_file)

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
