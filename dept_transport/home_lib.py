"""
Home Lib.py
Generic Library
"""
import logging

import collections
import csv
import mmap
import os
import socket
import platform
import tabulate
import difflib
from pathlib import Path

import re
import sys
import time
from datetime import datetime
import pyodbc
import pandas as pd
import numpy as np
# import racq_conn_lib as rqconnlib

# --------------------------------------------------------------------
#
#                          Constants
#
# --------------------------------------------------------------------

# global dict TEST_RESULT_DIRS is created by fetch_log_dirs and contains the following entried:
# TEST_RESULT_DIRS['log']
# TEST_RESULT_DIRS['data']
# TEST_RESULT_DIRS['error']
# TEST_RESULT_DIRS['commands']
# TEST_RESULT_DIRS['reports']

SUCCESS = 0
FAIL_GENERIC = -1
FAIL_NO_DB_CONNECT = -2
DAYS_FOR_DEEP_ANALYSE = 5

CONFIG_DIR = '/home/user/Dropbox/config'
SAVE_DIR = '{}/{}'.format(CONFIG_DIR, 'saved_info')
SAVE_REP = '{}/{}'.format(CONFIG_DIR, 'reports')

EMAIL_DEFAULT = 'proetman@gmail.com.au'


MAIL_HEADER = """\
<html>
<body>
<pre style="font: monospace">
"""

MAIL_HEADER_WITH_BORDER = """\
<html>
<body>
<style>
table {
    border-collapse: collapse;
}
table, th, td {
    border: 1px solid black;
}
</style>
<pre style="font: monospace"
>
"""

MAIL_FOOTER = """\
</pre>
</body>
</html>
"""

MAIL_FROM_USER = 'noreply@gmail.com'
# --- fetch config files
# --------------------------------------------------------------------
#
#                          Fetch Rego Plats
#
# --------------------------------------------------------------------


def fetch_rego_plates():
    """
    fetch all number plates from the rego.csv file
    """
    csv_file = '{}/{}'.format(CONFIG_DIR, 'rego.csv')
    csv_data = []

    header = True
    with open(csv_file) as csvfile:
        f = csv.reader(csvfile, delimiter=',')

        for row in f:
            if header:
                header = False
                continue
            csv_data.append(row)
            # print(row)

    return csv_data









# --- Init
# --------------------------------------------------------------------
#
#                          validate dir param
#
# --------------------------------------------------------------------


def validate_dir_param(p_dir):
    """
    validate directory parameter does not have back slash
    validate trailing char is not forward slash.
    """
    log_debug('start valdate dir param [{}]'.format(p_dir))
    l_dir = p_dir

    l_dir = l_dir.replace('\\', '/')
    last_char = l_dir[-1]
    if last_char == '/':
        l_dir = l_dir[:-1]

    log_debug('end valdate dir param [{}]'.format(l_dir))
    return l_dir

# --------------------------------------------------------------------
#
#                          init (every program should run this)
#
# --------------------------------------------------------------------


def init_app(p_args, p_print_date=True):

    global g_params
    # g_params = {}

    g_params = p_args

#    systest_conn_d = rqconnlib.db_conn_syst()
#    if systest_conn_d is None:
#        return False

    g_params['run_date_str'] = time.strftime("%d/%m/%Y")
    g_params['run_time_str'] = time.strftime("%H:%M:%S")
    # g_params['osuser'] = os.getlogin()
    g_params['local_host'] = socket.gethostname()

    if p_print_date:
        # Display the run date, this will end up in the .out files to delimit each days run.
        run_datetime = time.strftime("%d-%m-%Y %H:%M:%S")
        p_i('Run Date: {}'.format(run_datetime))

    return True

# --------------------------------------------------------------------
#
#                          init email
#
# --------------------------------------------------------------------

def init_email():
    """ Initialize the email config """

    email_config_file = '{}/{}'.format(CONFIG_DIR, 'email.txt')
    with open(email_config_file) as email_file:
        content = email_file.readlines()

    content = [x.strip() for x in content]

    if len(content[1]) == 0:
        return None

    email_config = {}
    email_config['from'] = content[0]
    email_config['pass'] = content[1]
    email_config['to'] = content[2]

    return email_config



# --------------------------------------------------------------------
#
#                          init (every program should run this)
#
# --------------------------------------------------------------------


def init():
    global g_params
    g_params = {}

    # Display the run date, this will end up in the .out files to delimit each days run.
    run_datetime = time.strftime("%d-%M-%Y %H:%M:%S")
    p_i('Run Date: {}'.format(run_datetime))

    return

# --------------------------------------------------------------------
#
#                          safe upper
#
# --------------------------------------------------------------------


def safe_upper(p_str):
    """ Convert str to upper case"""
    new_str = None
    if p_str is not None:
        if isinstance(p_str, str):
            new_str = p_str.upper()

    return new_str


def safe_lower(p_str):
    """ Convert str to lower case"""
    new_str = None

    if p_str is not None:
        if isinstance(p_str, str):
            new_str = p_str.lower()

    return new_str


# --- OS paths etc
# --------------------------------------------------------------------
#
#                          fetch arg numb
#
# --------------------------------------------------------------------


def fetch_arg_numb(p_name):
    """
    Find the number for this argument.
    return the number, and the value (if it exists)
    """
    argind = 0

    try:

        while sys.argv[argind] != p_name:
            argind += 1

    except IndexError:
        argind = 0

    if argind > 0 and argind < len(sys.argv) - 1:
        retval = sys.argv[argind + 1]
    else:
        retval = None

    return argind, retval

# --------------------------------------------------------------------
#
#                          Fetch arg Name
#
# --------------------------------------------------------------------


def fetch_arg_name():

    # -- Load TAB

    argind, retval = fetch_arg_numb('--tab')

    # -- if that fails, try loading account name
    if argind == 0:
        argind, retval = fetch_arg_numb('--account_name')

    # -- if that fails, try loading account name
    if argind == 0:
        argind, retval = fetch_arg_numb('--account')

    # -- if that fails, try loading run_all_accounts
    #    if argind == 0:
    #        argind, retval = fetch_arg_numb('--run_all_accounts')

    if argind == 0:
        print('ERROR: must select at least one of these parameters:')
        print('          tab, account_name or account')
        print('      aborting.')
        retval = None
    else:
        print('')
        print('    Process: {}'.format(retval))
        print('')

    return retval

# --------------------------------------------------------------------
#
#                          Fetch arg Name
#
# --------------------------------------------------------------------


def fetch_arg_name2():

    argind, retval = fetch_arg_numb('--help')
    if argind != 0:
        return 'help'

    argind, retval = fetch_arg_numb('--account')

    if argind == 0:
        print('ERROR: must select an ACCOUNT to run:')
        print('      aborting.')
        retval = None
    else:
        print('')
        print('    Process: {}'.format(retval))
        print('')

    return retval


# --------------------------------------------------------------------
#
#                          Setup RESULT dir
#
# --------------------------------------------------------------------


def setup_result_dir(p_root, p_dir):
    """
    Create dir if required.
    Add dir to global arrary.
    """

    new_path = p_root + p_dir
    if dir_create(new_path):
        TEST_RESULT_DIRS[p_dir] = new_path

    return

# --------------------------------------------------------------------
#
#                          log dir fetch
#
# --------------------------------------------------------------------


def fetch_log_dirs():
    """ Fetch a list of subfolder names to be used for logging
    If needed, create the subfolders"""

    # this is generally called during initialise, so debugging has not
    # yet been enabled.

    # log_debug('Start log fetch_dirs')

    home_dir = str(Path.home())

    l_root =  f"{home_dir}/test_results/"

    global TEST_RESULT_DIRS
    TEST_RESULT_DIRS = {}

    setup_result_dir(l_root, 'log')
    setup_result_dir(l_root, 'data')
    setup_result_dir(l_root, 'commands')
    setup_result_dir(l_root, 'error')
    setup_result_dir(l_root, 'reports')
    setup_result_dir(l_root, 'tmp')

    return TEST_RESULT_DIRS


# --- OS db Commands
# --------------------------------------------------------------------
#
#                          Search File for String (RE)
#
# --------------------------------------------------------------------


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

# --------------------------------------------------------------------
#
#                          Rename File
#
# --------------------------------------------------------------------


def file_rename(p_old_file, p_new_file):
    """
    Rename file OldFileName -> NewFileName
         file_rename(Old,New)
    If the new file already exists, return False.
    If the old file does not exist, return False.
    If there is a catastrophic fail, exit.
    Otherwise - return True!
    """

    log_debug('start file_rename')

    if os.path.isfile(p_new_file):
        return False

    if os.path.isfile(p_old_file):

        try:
            os.rename(p_old_file, p_new_file)

        except OSError as err:
            print("\nFailed to rename file {0} to {1}, aborting\n".
                  format(p_old_file, p_new_file))
            print("OS Error({0}): {1}".format(err.errno, err.strerror))
            print("\n")
            exit(2)

        return True

    return False

# --------------------------------------------------------------------
#
#                          Remove File
#
# --------------------------------------------------------------------


def file_remove(p_file):
    """
    Delete file
    """
    log_debug('start file_remove')

    if os.path.isfile(p_file):

        try:
            os.remove(p_file)

        except OSError as err:
            print("\nFailed to remove file :{0}, aborting\n")
            print("OS Error({0}): {1}".format(err.errno, err.strerror))
            print("\n")
            exit(2)


# --------------------------------------------------------------------
#
#                          create empty file
#
# --------------------------------------------------------------------


def file_touch(path):
    """
    update timestamp of a file
    or create empty file.
    """
    with open(path, 'a'):
        os.utime(path, None)

# --------------------------------------------------------------------
#
#                          tail
#
# --------------------------------------------------------------------


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
# --------------------------------------------------------------------
#
#                          fetch python root dir
#
# --------------------------------------------------------------------


def fetch_root_dir():
    """ Fetch the location of the directory "Final"   """

    python_root_dir = os.environ['PYTHONPATH'][:-9]
    python_root_dir = python_root_dir.replace('\\', '/')

    return python_root_dir

# --------------------------------------------------------------------
#
#                          fetch final dir
#
# --------------------------------------------------------------------


def fetch_final_dir():
    """ Fetch the location of the directory "Final"   """

    log_debug('Fetch final dir')
    result = '{}/{}'.format(fetch_root_dir(), 'Final')
    log_debug('  final dir [{}]'.format(result))

    return result

# --------------------------------------------------------------------
#
#                          fetch final dir
#
# --------------------------------------------------------------------


def fetch_info_class_dir():
    """ Fetch the location of the directory "Final"   """

    log_debug('Fetch info class dir')
    result = '{}/{}'.format(fetch_root_dir(), 'Final/classification_validation')
    log_debug('  info class dir [{}]'.format(result))

    return result


# --------------------------------------------------------------------
#
#                          safe open
#
# --------------------------------------------------------------------


def safe_open(p_file_name, p_mode):
    """
    Open the file.
    print error message to log file if fail.
    """
    try:
        result = open(p_file_name, p_mode)

    # File does not exist (yet), must be first run!
    except IOError as e:
        result = None
        p_e('Failed to open file [{}]'.foramt(p_file_name))
        p_e('    error raised: {}'.format(e))

    return result


# --------------------------------------------------------------------
#
#                          generate file name
#
# --------------------------------------------------------------------
# Create a full path file name from the directory and the file name
#   only here as we have multiple OS to work with.


def file_generate_name(p_dir, p_file):
    """
    create filename with respect to OS considerations.
    """

    log_debug('start gen_filename')
    return p_dir + '/' + p_file

# --------------------------------------------------------------------
#
#                          Return Date Time string for filename
#
# --------------------------------------------------------------------


def now():
    """
    Return Date_Time as a string %Y%m%d_%H%M%S
    """
    return time.strftime("%Y%m%d_%H%M%S")

    # --------------------------------------------------------------------
#
#                          Return Date Time with MS string for filename
#
# --------------------------------------------------------------------


def now_with_ms():
    """
    Return Date_Time as a string %Y%m%d_%H%M%S_ms
    """

    curr = datetime.now()
    microsec = curr.microsecond
    return '{}_{}'.format(time.strftime("%Y%m%d_%H%M%S"), microsec)

# --------------------------------------------------------------------
#
#                          is Windoze
#
# --------------------------------------------------------------------


def is_windows():
    """
    Determine if running on windows box
    """
    log_debug('start isWindows')

    return platform.system() == 'Windows'

# --------------------------------------------------------------------
#
#                          Remove Dir
#
# --------------------------------------------------------------------


def dir_remove(p_dir):
    """
    remove directory
    Assumes directory is empty
    Full path name required.
    """
    log_debug('start remove_dir')

    if os.path.isdir(p_dir):

        try:
            os.rmdir(p_dir)

        except OSError as err:
            print("\nFailed to remove directory :{0}, aborting\n")
            print("OS Error({0}): {1}".format(err.errno, err.strerror))
            print("\n")
            exit(2)

# --------------------------------------------------------------------
#
#                          fetch Work Dir
#
# --------------------------------------------------------------------


def dir_fetch_workdir():
    """
    Fetch the current working directory
    """
    log_debug('start fetchwork_dir')
    work_dir = TEST_RESULT_DIRS['log']
    if is_windows():
        work_dir = work_dir.replace('\\', '/')

    return work_dir

# --------------------------------------------------------------------
#
#                          Create Dir
#
# --------------------------------------------------------------------


def dir_create(p_dir):
    """
    Create Directory
    """
    log_debug('start create_dir')

    if os.path.isdir(p_dir):
        return True
    else:
        try:
            os.makedirs(p_dir)

        except OSError as err:
            log_warning("\nFailed to create directory :{0}, aborting\n")
            log_warning("OS Error({0}): {1}".format(err.errno, err.strerror))
            log_warning("\n")
            return False

        except PermissionError as err:
            p_e('Failed to create LOG directory: {}'.format(p_dir))
            p_e('OS error: {}'.format(err))
            return False

    return True

# --------------------------------------------------------------------
#
#                          validate args
#
# --------------------------------------------------------------------


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

# --- Create Mail

# --------------------------------------------------------------------
#
#                         write line to file
#
# --------------------------------------------------------------------


def write_line_to_file(p_file, p_line, p_include_timestamp):
    """
    Write the line to the file, including timestamp if requested.
    """
    if p_include_timestamp:
        p_file.write(p_line)
    else:
        p_file.write(p_line[35:])

    return


# --------------------------------------------------------------------
#
#                         write_line_containing
#
# --------------------------------------------------------------------


def write_line_containing(p_source_txt, p_target_txt, p_text, p_include_timestamp=True):
    """
   Open the source txt file with read only permit  and Read each line.
   if the line contains the supplied text then write that line to the target txt
   """
    l_log = open(p_source_txt)
    line = l_log.readline()
    while line:
        if p_text in line:
            write_line_to_file(p_target_txt, line, p_include_timestamp)
        line = l_log.readline()
    l_log.close()
    return

# --------------------------------------------------------------------
#
#                         write_line_containing
#
# --------------------------------------------------------------------


def write_line_not_containing(p_source_txt, p_target_txt, p_text_dict, p_include_timestamp=True):
    """
   Open the source txt file with read only permit  and Read each line.
   if the line contains the supplied text then write that line to the target txt
   """
    l_log = open(p_source_txt)
    line = l_log.readline()
    while line:

        include_line = True

        for txt in p_text_dict:
            if txt in line:
                include_line = False
                break

        if include_line:
            write_line_to_file(p_target_txt, line, p_include_timestamp)

        line = l_log.readline()

    l_log.close()

    return

# --------------------------------------------------------------------
#
#                         write_chunk_from_to
#
# --------------------------------------------------------------------


def write_chunk_from_to(p_source_txt, p_target_txt, p_text_from, p_text_to,
                        p_include_timestamp=True):
    """
   Open the source txt file with read only permit  and Read each line.
   if the line contains the supplied text then write that line to the target txt
   """
    l_log = open(p_source_txt)
    line = l_log.readline()
    while line:
        if p_text_from in line:
            while p_text_to not in line:

                write_line_to_file(p_target_txt, line, p_include_timestamp)

                line = l_log.readline()
        else:
            line = l_log.readline()

    l_log.close()
    return

# --- Logging
# --------------------------------------------------------------------
#
#                          display filename
#
# --------------------------------------------------------------------


def format_filename(p_file):
    """ format filename with backslash, not forward slash """
    return p_file.replace('/', '\\')

# --------------------------------------------------------------------
#
#                          Print and DEbug
#
# --------------------------------------------------------------------


def p_d(p_str, p_end=None):
    """
    print str to screen
    and print to debug
    """
    if p_end is None:
        print(p_str)
    else:
        print(p_str, end=p_end)
    log_debug(p_str)

# --------------------------------------------------------------------
#
#                          Print and Error
#
# --------------------------------------------------------------------


def p_e(p_str, p_end=None, p_before=None, p_after=None):
    """
    print str to screen
    and print to debug
    """
    if p_before is not None:
        for i in range(0, p_before):
            log_error('')

    if p_end is None:
        print(p_str)
    else:
        print(p_str, end=p_end)
    log_error(p_str)

    if p_after is not None:
        for i in range(0, p_after):
            log_error('')

# --------------------------------------------------------------------
#
#                          Print and Error
#
# --------------------------------------------------------------------


def p_c(p_str, p_end=None):
    """
    print str to screen
    and print to debug
    """
    if p_end is None:
        print(p_str)
    else:
        print(p_str, end=p_end)
    log_error(p_str)

# --------------------------------------------------------------------
#
#                          Print and Info
#
# --------------------------------------------------------------------


def p_i(p_str, p_end=None, p_before=None, p_after=None):
    """
    print str to screen
    and print to debug
    """
    if p_before is not None:
        for i in range(0, p_before):
            log_info('')

    if p_end is None:
        print(p_str)
    else:
        print(p_str, end=p_end)
    log_info(p_str)

    if p_after is not None:
        for i in range(0, p_after):
            log_info('')

# --------------------------------------------------------------------
#
#                          Shutdown logging
#
# --------------------------------------------------------------------


def logging_close():
    """
    Close the logging file name
    Mainly used for unit testing, when a log file is opened for each test
    """
    logging.shutdown()
# --------------------------------------------------------------------
#
#                          fetch Work Dir
#
# --------------------------------------------------------------------


def log_filename_determine(p_work_dir, p_program):
    """
    Fetch log file name
    """
    log_debug('start log_filename_determine')

    # Get the time in milliseconds
    curr = datetime.now()
    debug_microsec = curr.microsecond

    debug_datetime = time.strftime("%Y%m%d_%H%M%S")

    log_file_template = '{vwDir}/{vProg}_{vDT}_{vMS}.log'

    log_file = log_file_template.format(vwDir=p_work_dir,
                                        vProg=p_program,
                                        vDT=debug_datetime,
                                        vMS=debug_microsec)
    return log_file

    # This is no longer required, switched over to including microseconds
    # in the file name. That will always be unique.
    #
    # Have done this so that the "sleep 1" commands can be removed from unit testing.
    #
    #    if os.path.isfile(log_file):
    #
    #        # ascii 97,123 is 'a' to 'z'
    #        for character in range(97, 123):
    #            log_file = log_file_template2.format(vwDir=p_work_dir,
    #                                                 vProg=p_program,
    #                                                 vDT=debug_datetime,
    #                                                 vChar=chr(character))
    #
    #            # if the file does not exist, then break out of loop.
    #            # have a filename that can be used for logging.
    #            if not os.path.isfile(log_file):
    #                break


# --------------------------------------------------------------------
#
#                          init log file
#
# --------------------------------------------------------------------


def log_filename_init(over_ride_name=None):
    """
    Determine log file name
       default parameter is none, will then create a file with
       the program name as the basis for the file.
    """
    #
    # Strip off any leading path to the program executable
    #          remove  "c:/tmp" from "c:/tmp/prog.py".
    #          Leaves prog.py
    #
    # Then split of the first part of the program name
    #          prog.py  --> prog
    #
    fetch_log_dirs()
    if over_ride_name is None:
        program_name = sys.argv[0].split("/")[-1]
    else:
        program_name = over_ride_name

    program_base_name = os.path.basename(program_name).split('.')[0]

    # --------------------------------------------
    # Setup Debug Info

    work_dir = dir_fetch_workdir()

    if not dir_create(work_dir):
        return None
    log_filename = log_filename_determine(work_dir, program_base_name)

    return log_filename

# --------------------------------------------------------------------
#
#                          log Level
#
# --------------------------------------------------------------------


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

# --------------------------------------------------------------------
#
#                          log Args
#
# --------------------------------------------------------------------


def log_args(p_args):
    """
    Print all arguments
    """
    # If there are no argments, do nothing.
    if len(p_args) > 0:

        # Display heading
        log_info("\n")
        log_info("Display program arguments")
        log_info("-------------------------")
        log_info("{0:<30s} {1:<50s}".format('Argument', 'Value'))
        log_info("{0:<30s} {1:<50s}".format('------------------------------',
                 '--------------------------------------------------'))
        ord_args = collections.OrderedDict(sorted(p_args.items()))
        # Display Arguments
        for arg in ord_args:
            if isinstance(ord_args[arg], bool):
                if ord_args[arg]:
                    log_info("{0:<30s} {1:<50s}".format(arg, 'True'))
                else:
                    log_info("{0:<30s} {1:<50s}".format(arg, 'False'))
            else:
                log_info("{0:<30s} {1!s:<50s}".format(arg, ord_args[arg]))

        log_info("\n")

# ----------------------------------------------------------------
#
#                 log {Level}
#
# ----------------------------------------------------------------


def log_critical(print_string):
    """
    Log Critical Error message to file and screen
    """
    logging.critical(print_string)
    print("\n{}\n".format(print_string))


def log_debug(print_string):
    """ Debug to log file """
    # print('debuging this str {}'.format(str))
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

# --- Debug Stuff
# --------------------------------------------------------------------
#
#                          debug results
#
# --------------------------------------------------------------------


def debug_results(p_type, p_s_df, p_t_df, p_tab):
    """
    This routine is for debugging data only, it should not be used for displaying
    any results.
    The routines are to find differences in data, to assist with coding issues
    (eg comparing NaN to None, looking for unprintable char, etc)
    """

    log_debug('Start debug results2')

    if p_type is None:
        log_debug('Debug Type is None, doing nothing')

    elif p_type == 'a':
        debug_test_a(p_s_df, p_t_df)

    elif p_type == 'b':
        debug_test_b(p_s_df, p_t_df)

    elif p_type == 'c':
        debug_test_c(p_s_df, p_t_df, p_tab)

    elif p_type == 'c1':
        debug_test_c_deep1(p_s_df, p_t_df, p_tab)

    elif p_type == 'c2':
        debug_test_c_deep2(p_s_df, p_t_df, p_tab)

    elif p_type == 'd':
        debug_test_d(p_s_df, p_t_df, p_tab)

    return

# --------------------------------------------------------------------
#
#                          debug test
#
# --------------------------------------------------------------------


def debug_test_a(p_csv_df, p_tab_df):
    """
    Remove one column at a time, and run the comparison.
    When the error count drops considerably, you have found the problem child column.
    """
    new_cols = list(p_csv_df.columns)

    # p_tab_df.fillna(value=np.nan, inplace=True)

    csv_rem_df, tab_rem_df = tab_compare_del_common(p_csv_df, p_tab_df)
    error_count = len(csv_rem_df.index)
    p_d('test cols = {} (none removed)'.format(new_cols))
    p_d('    error count = {}'.format(error_count))

    while len(new_cols) > 1:
        new_cols = new_cols[:-1]
        p_d('test cols = {}'.format(new_cols))
        new_csv_df = p_csv_df[new_cols]
        new_tab_df = p_tab_df[new_cols]

        csv_rem_df, tab_rem_df = tab_compare_del_common(new_csv_df, new_tab_df)
        error_count = len(csv_rem_df.index)
        p_d('    error count = {}'.format(error_count))

    return
# --------------------------------------------------------------------
#
#                          debug test 3
#
# --------------------------------------------------------------------


def debug_test_b(pd1, pd2):
    """
    Remove one column at a time, and run the comparison.
    When the error stops getting raised, you have found the problem child column.
    (i.e. the column that raised a value error when running a comparison of DF's)
    """

    new_cols = list(pd1.columns)

    while len(new_cols) > 1:
        new_cols = new_cols[:-1]
        p_d('test cols = {}'.format(new_cols))

        new_csv_df = pd1[new_cols]
        new_tab_df = pd2[new_cols]

        try:
            eql = ((new_csv_df == new_tab_df) | ((new_csv_df != new_csv_df) &
                                                 (new_tab_df != new_tab_df)))

            p_d('len of eq1 is {}'.format(len(eql.index)))

        except ValueError:
            p_d('Failed on value error')

    return


# --------------------------------------------------------------------
#
#                          debug test
#
# --------------------------------------------------------------------


def debug_test_c(p_csv_df, p_tab_df, p_tab):
    """
    Loop through each column and run the comparison
    """
    new_cols = list(p_csv_df.columns)
    p_d('len of new list is {}'.format(len(new_cols)))

    for col in new_cols:
        p_d('Processing column {}'.format(col))

        new_csv_df = p_csv_df[col].to_frame()
        new_tab_df = p_tab_df[col].to_frame()
        csv_rem_df, tab_rem_df = tab_compare_del_common(new_csv_df, new_tab_df)
        error_count = len(csv_rem_df.index) + len(tab_rem_df.index)
        p_d('    Debug_test2 column {}, error_count = {}'.format(col, error_count))
        if error_count > 0:
            log_error('        Errors found on tab.col {}.{} = {}'
                      .format(p_tab, col, error_count))

    return

# --------------------------------------------------------------------
#
#                          debug test
#
# --------------------------------------------------------------------


def debug_test_c_deep1(p_csv_df, p_tab_df, p_tab):
    """
    This code is derived from debug_test2,
    It can be used where the two rows that are being compared are from the same Primary key.
    It does a very thorough comparison of the fields.
    """

    new_cols = list(p_csv_df.columns)
    p_d('len of new list is {}'.format(len(new_cols)))

    for col in new_cols:
        p_d('Processing column {}'.format(col))

        new_csv_df = p_csv_df[col].to_frame()
        new_tab_df = p_tab_df[col].to_frame()
        csv_rem_df, tab_rem_df = tab_compare_del_common(new_csv_df, new_tab_df)
        error_count = len(csv_rem_df.index) + len(tab_rem_df.index)
        p_d('    Debug_test4 column {}, error_count = {}'.format(col, error_count))
        if error_count > 0:
            log_error('        Errors found on tab.col {}.{} = {}'
                      .format(p_tab, col, error_count))

            # NOTE: this only works when the different rows match on both sides
            # otherwise use the next for loop.
            for i, row in csv_rem_df.iterrows():
                p_d('            processing row {}'.format(i))
                src = csv_rem_df[col][i]
                trg = tab_rem_df[col][i]

                if isinstance(src, int) or isinstance(trg, int):
                    pass
                else:
                    for pos, rrow in enumerate(difflib.ndiff(src, trg)):
                        if rrow[0] == ' ':
                            continue
                        elif rrow[0] == '-':
                            p_d(u'                Delete "{}" from position {} ({})'.
                                format(rrow[-1], pos, ord(rrow[-1])))
                        elif rrow[0] == '+':
                            p_d(u'                Add "{}" to position {} ({})'.
                                format(rrow[-1], pos, ord(rrow[-1])))

    return

# --------------------------------------------------------------------
#
#                          debug test
#
# --------------------------------------------------------------------


def debug_test_c_deep2(p_csv_df, p_tab_df, p_tab):
    """
    This code is derived from debug_test2 and debug_test4,
    It can be used where the two rows that are being compared are from the same Primary key.
    It does a very thorough comparison of the fields.
    """

    new_cols = list(p_csv_df.columns)
    p_d('len of new list is {}'.format(len(new_cols)))

    for col in new_cols:
        p_d('Processing column {}'.format(col))

        new_csv_df = p_csv_df[col].to_frame()
        new_tab_df = p_tab_df[col].to_frame()
        csv_rem_df, tab_rem_df = tab_compare_del_common(new_csv_df, new_tab_df)
        error_count = len(csv_rem_df.index) + len(tab_rem_df.index)
        p_d('    Debug_test4 column {}, error_count = {}'.format(col, error_count))
        if error_count > 0:
            log_error('        Errors found on tab.col {}.{} = {}'
                      .format(p_tab, col, error_count))

            # this loop is much slower, as it compares EVERY row in the original dataframe
            # use the previous loop to just compare differences.

            for row, idx in new_csv_df.iterrows():
                p_d('            processing row {}'.format(row))
                src = new_csv_df[col][idx]
                trg = new_tab_df[col][idx]

                if isinstance(src, int) or isinstance(trg, int):
                    pass
                else:
                    if src is not None and trg is not None:
                        for pos, rrow in enumerate(difflib.ndiff(src, trg)):
                            if rrow[0] == ' ':
                                continue
                            elif rrow[0] == '-':
                                p_d(u'                Delete "{}" from position {} ({})'.
                                    format(rrow[-1], pos, ord(rrow[-1])))
                            elif rrow[0] == '+':
                                p_d(u'                Add "{}" to position {} ({})'.
                                    format(rrow[-1], pos, ord(rrow[-1])))

    return
# --------------------------------------------------------------------
#
#                          debug test d
#
# --------------------------------------------------------------------


def debug_test_d(p_csv_df, p_tab_df, p_tab):
    """
    similar to test_c, but first remove the rows that do not have a common PK

    """
    new_cols = list(p_csv_df.columns)
    p_d('len of new list is {}'.format(len(new_cols)))

    for col in new_cols:
        p_d('Processing column {}'.format(col))

        new_csv_df = p_csv_df[col].to_frame()
        new_tab_df = p_tab_df[col].to_frame()
        csv_rem_df, tab_rem_df = tab_compare_del_common(new_csv_df, new_tab_df)
        error_count = len(csv_rem_df.index) + len(tab_rem_df.index)
        p_d('    Debug_test4 column {}, error_count = {}'.format(col, error_count))
        if error_count > 0:
            log_error('        Errors found on tab.col {}.{} = {}'
                      .format(p_tab, col, error_count))

            # NOTE: this only works when the different rows match on both sides
            # otherwise use the next for loop.
            for i, row in csv_rem_df.iterrows():
                p_d('            processing row {}'.format(i))
                src = csv_rem_df[col][i]
                trg = tab_rem_df[col][i]

                if isinstance(src, int) or isinstance(trg, int):
                    pass
                else:
                    for pos, rrow in enumerate(difflib.ndiff(src, trg)):
                        if rrow[0] == ' ':
                            continue
                        elif rrow[0] == '-':
                            p_d(u'                Delete "{}" from position {} ({})'.
                                format(rrow[-1], pos, ord(rrow[-1])))
                        elif rrow[0] == '+':
                            p_d(u'                Add "{}" to position {} ({})'.
                                format(rrow[-1], pos, ord(rrow[-1])))

    return

# --- eof ---
