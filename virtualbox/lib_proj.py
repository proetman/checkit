from __future__ import division
from __future__ import print_function

# Import OS Functions
import argparse
import datetime
import logging
import platform
import re

# import math


# ----------------------------------------------------------------------------------------------------
#
#                                           Constants
#
# ----------------------------------------------------------------------------------------------------

SUCCESS=0
FAIL=1


# ----------------------------------------------------------------------------------------------------
#
#                                       Search File for String (RE)
#
# ----------------------------------------------------------------------------------------------------


def file_search(curr_file_name, search_string):
    """
    Search for a string in a file with regular expression search
    Return Codes
        True - String Found
        False - String Not Found

        If the file does not exist, or there is any other fail, return False

    Note: cannot do a case insensitive search on an entire file.
    """
    # Test if the file exists
    # Test if the file has size > 0 (mmap failes on filesize == 0)

    if os.path.isfile(curr_file_name) and os.stat(curr_file_name).st_size > 0:

        try:
            my_file = open(curr_file_name, 'r+')
        except FileNotFoundError as err:
            print('ERROR: File not found in fileSearch')
            print('       filename : {}'.format(curr_file_name))
            print('       error details : {}'.format(err))
            return False

        search_string_bytes = bytes(search_string, 'utf-8')
        data = mmap.mmap(my_file.fileno(), 0)
        my_search_result = re.search(search_string_bytes, data)

        my_file.close()

        if my_search_result:
            return True

    return False

# ----------------------------------------------------------------------------------------------------
#
#                                                tail
#
# ----------------------------------------------------------------------------------------------------


def file_tail(file_name):
    """
       Read the last line of a file
    """
    try:
        my_file = open(file_name, 'r')
        try:
            result = collections.deque(my_file, 1).pop()
        except IndexError as coll_err:
            print('ERROR Reading last line of file')
            print('       error details : {}'.format(coll_err))
            result = ''
        my_file.close()

    # File does not exist (yet), must be first run!
    except FileNotFoundError:
        result = ''

    return result

# ----------------------------------------------------------------------------------------------------
#
#                                               is Windoze
#
# ----------------------------------------------------------------------------------------------------


def is_windows():
    """
    Determine if running on windows box
    """
    log_debug('start isWindows')

    return platform.system() == 'Windows'


# ----------------------------------------------------------------------------------------------------
#
#                                             validate args
#
# ----------------------------------------------------------------------------------------------------


def args_validate(p_parser, p_log_file):
    """
    Validate program arguments
    """
    # Setup Arguments and parse them

    args = vars(p_parser.parse_args())

    # Setup Logging

    logging_level = log_level(args['debug'])

    if logging_level is not None:
        # Bug in spyder v2 and v3.
        # http://stackoverflow.com/questions/24259952/logging-module-does-not-print-in-ipython
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)

        logging.basicConfig(level=logging_level,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=p_log_file,
                            filemode='w')

        log_info('\n')
        log_info('rs_lib.validate_args: Logging level: [{}]'.format(logging_level))

        print("\nprogram log_file: " + p_log_file.replace('/', '\\') + "\n")

    # print the arguments to log file at level INFO
    log_args(args)

    return args


# ----------------------------------------------------------------------------------------------------
#
#                          Print and send to DEBUG
#
# ----------------------------------------------------------------------------------------------------


def p_d(p_str):
    """
    print str to screen
    and print to debug
    """
    print(p_str)
    log_debug(p_str)

# ----------------------------------------------------------------------------------------------------
#
#                          Print and send to ERROR
#
# ----------------------------------------------------------------------------------------------------


def p_e(p_str):
    """
    print str to screen
    and print to debug
    """
    print(p_str)
    log_error(p_str)


# ----------------------------------------------------------------------------------------------------
#
#                          Shutdown logging
#
# ----------------------------------------------------------------------------------------------------


def logging_close():
    """
    Close the logging file name
    Mainly used for unit testing, when a log file is opened for each test
    """
    logging.shutdown()


# ----------------------------------------------------------------------------------------------------
#
#                          log Level
#
# ----------------------------------------------------------------------------------------------------


def log_level(p_level):
    """
    Determine the Log Level for debug
    """

    # Determine the logging level

    if p_level == 'DEBUG':
        return_code = logging.DEBUG

    elif p_level == 'INFO':
        return_code = logging.INFO

    elif p_level == 'WARNING':
        return_code = logging.WARNING

    elif p_level == 'ERROR':
        return_code = logging.ERROR

    elif p_level == 'CRITICAL':
        return_code = logging.CRITICAL

    elif p_level == 'NONE':
        return_code = None

    else:
        print('ERROR: Failed to set correct debug level - aborting')
        exit(1)

    return return_code

# ----------------------------------------------------------------------------------------------------
#
#                          log Args
#
# ----------------------------------------------------------------------------------------------------


def log_args(p_args):
    """
    Print all arguments to logfile.
    """

    log_template = "{0:<20s} {1:<50s}"
    # If there are no argments, do nothing.
    if len(p_args) > 0:

        # Display heading
        log_info("\n")
        log_info("Program arguments")
        log_info("-----------------")
        log_info(log_template.format('Arg', 'Value'))

        # Display Arguments
        for arg in p_args:
            if isinstance(p_args[arg], bool):
                if p_args[arg]:
                    log_info(log_template.format(arg, 'True'))
                else:
                    log_info(log_template.format(arg, 'False'))
            else:
                log_info(log_template.format(arg, ''))
                log_info(log_template.format(arg, p_args[arg]))

        log_info("\n")

# ----------------------------------------------------------------------------------------------------
#
#                 log {Level}
#
# ----------------------------------------------------------------------------------------------------


def log_critical(print_string):
    """ Log Critical Error message to file and screen """
    logging.critical(print_string)
    print("\n{}\n".format(print_string))


def log_debug(print_string):
    """ Debug to log file """
    logging.debug(print_string)


def log_info(print_string):
    """ Info to log file """
    logging.info(print_string)


def log_warning(print_string):
    """ Warning to log file """
    logging.warning(print_string)


def log_error(print_string):
    """ Error  to log file """
    logging.error(print_string)

# --- eof ---
