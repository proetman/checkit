#!/usr/local/bin/python3

import os
import re
import string
import logging
import time
import argparse


# --------------------------------------------------------------------
#
#                          Init Log Filename
# 
# --------------------------------------------------------------------

# Setup a log file name
# Remove all spaces from file name

def init_log_filename(p_program, p_name, p_datetime):

    l_filename = p_program + '_' + p_name + '_' + p_datetime + '.log'
    # l_filename = 'x' + '_' + p_name + '_' + p_datetime + '.log'
    l_filename = l_filename.replace(' ','')                       
    return(l_filename)
    
# --------------------------------------------------------------------
#
#                          Initialize Arguments
# 
# --------------------------------------------------------------------

def initialize_arguments(p_parser, p_program_name, p_datetime):

    p_parser.add_argument('-d','--debug', \
        help=' Log messages with increasing levels of verbosity CRITICAL (least) to DEBUG (most)', \
        choices=('NOTSET', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'), \
        default="NOTSET", \
        required=False)

    args = vars(p_parser.parse_args())

    if args['debug'] == 'DEBUG':
        logging_level = logging.DEBUG
    elif args['debug'] == 'INFO':
        logging_level = logging.INFO
    elif args['debug'] == 'WARNING':
        logging_level = logging.WARNING
    elif args['debug'] == 'ERROR':
        logging_level = logging.ERROR
    elif args['debug'] == 'CRITICAL':
        logging_level = logging.CRITICAL
    elif args['debug'] == 'NOTSET':
        logging_level = logging.NOTSET
    else:
        print('ERROR: Failed to set correct debug level - aborting');
        exit(1)

    logging_filename = init_log_filename(p_program_name, args['name'], p_datetime ) 

    if logging_level == logging.NOTSET:
        print('No log file generated, try -d DEBUG for logging')
    else:
        # TODO: push directory into logging filename debug message.
        print('\nLog file - (need to include directory) [%s]\n' % logging_filename)


    logging.basicConfig(level=logging_level,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=logging_filename,
                        filemode='w')

    logging.info('utilities.init_migration: Logging level: [%s]' % (logging_level) )

    return(args)


