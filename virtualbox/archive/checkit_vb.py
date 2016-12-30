#!/usr/local/bin/python3

import os
import re
import string
import logging
import time
import argparse
import datetime
from time import  strftime
import subprocess
from   subprocess import CalledProcessError

from checkit_utility import  * 



# ----------------------------------------------------------------
#
#                 Global stuff
#
# ----------------------------------------------------------------


# ----------------------------------------------------------------
#
#                 Validate Arguments
#
# ----------------------------------------------------------------

def validate_arguments(p_args):
    null
    # logging.debug('start function validate_arguments')
    # logging.debug('p_args :' )
    # logging.debug(p_args)

    # logging.debug('end   function validate_arguments')

# ----------------------------------------------------------------
#
#                 M A I N
#
# ----------------------------------------------------------------

def main():

    program_name             = os.path.splitext(os.path.basename(__file__))[0] # remove path, then remove extension.
    local_home               = os.environ['HOME']                              # Get home directory
    start_datetime           = time.strftime("%Y%m%d_%H%M%S")                  # Startup time 
    start_datetime_display   = time.strftime("%H:%M:%S %d-%b-%Y")              # Startup time for Display

    # ----------------------------------------------------------------

    parser  = argparse.ArgumentParser('Run checkit virtual box')

    parser.add_argument('-n','--name',    help='Enter the name of the Virtual Box to check.',     required=True)
    parser.add_argument('-l','--logdir',  help='Enter the directory to write logs to.',           required=False)
    parser.add_argument('-c','--confdir', help='Enter the directory where the config files are.', required=False)

    initialize_arguments(parser, program_name, start_datetime)

#validate_standard_arguments(args)


# Get everything ready for the build
# run_id = build_init(db_conn, args['tag'], args['build_description'])

# print("Build Run ID: %d\n" % (run_id) )

# commit_db(db_conn)

# Run every migration
# run_migrations(db_conn, connect_str, run_id, args['migration_date'])

# Close down the build
# build_finalise(db_conn, run_id)

# commit_db(db_conn)

# disconnect_db(db_conn)

# ----------------------------------------------------------------

if __name__ == '__main__':
    main()

# --- eof ---
