#!/usr/bin/python

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

from utilities import  * 



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
    logging.debug('start function validate_arguments')
    logging.debug('p_args :' )
    logging.debug(p_args)

    logging.debug('end   function validate_arguments')

# ----------------------------------------------------------------
#
#                 Init Program - Global stuff
#
# ----------------------------------------------------------------

logging_filename = init_log_filename( 'template') 
print('\nLog file - [%s]\n' % logging_filename)

parser  = argparse.ArgumentParser('Run template program')

parser.add_argument('-u','--username', 
                    help='Enter the username', 
                    required=True)

parser.add_argument('-t','--tag', 
                    help='Tag for this build run, eg daily, one_off', 
                    required=False)

parser.add_argument('-b','--build_description', 
                    help='Description text for this build  run', 
                    required=False)

parser.add_argument('-m','--migration_date', 
                    help='Migration date for all programs (default: to end of today). Format dd-mm-yyyy hh24:mi:ss', 
                    default=default_migration_date,
                    required=False)


validate_arguments(args)
db_conn = connect_db(args['username'], ORACLE_SID) 
#
# The connect str is required for external connection (eg sqlldr)
db_password = FetchDBPassword(ORACLE_SID,args['username'])

connect_str = '%s/%s@%s' % ( args['username'], db_password, ORACLE_SID)

# Get everything ready for the build
run_id = build_init(db_conn, args['tag'], args['build_description'])

print("Build Run ID: %d\n" % (run_id) )

commit_db(db_conn)

# Run every migration
run_migrations(db_conn, connect_str, run_id, args['migration_date'])

# Close down the build
build_finalise(db_conn, run_id)

commit_db(db_conn)

disconnect_db(db_conn)

 



