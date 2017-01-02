from __future__ import division
from __future__ import print_function

# Import OS Functions
import argparse
import datetime
import os
import sys
import time

# Import project library
import lib_proj as lp

# ----------------------------------------------------------------------------------------------------
#
#                                           Constants
#
# ----------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------
#
#                                           Rename File
#
# ----------------------------------------------------------------------------------------------------


def file_rename(p_old_file, p_new_file):
    """
    Rename file OldFileName -> NewFileName
         file_rename(Old,New)
    If the new file already exists, return False.
    If the old file does not exist, return False.
    If there is a catastrophic fail, exit.
    Otherwise - return True!
    """

    lp.log_debug('start file_rename')

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

# ----------------------------------------------------------------------------------------------------
#
#                                            Remove File
#
# ----------------------------------------------------------------------------------------------------


def file_remove(p_file):
    """
    Delete file
    """
    lp.log_debug('start file_remove')

    if os.path.isfile(p_file):

        try:
            os.remove(p_file)

        except OSError as err:
            print("\nFailed to remove file :{0}, aborting\n")
            print("OS Error({0}): {1}".format(err.errno, err.strerror))
            print("\n")
            exit(2)


# ----------------------------------------------------------------------------------------------------
#
#                                           create empty file
#
# ----------------------------------------------------------------------------------------------------


def file_touch(path):
    """
    update timestamp of a file
    or create empty file.
    """
    with open(path, 'a'):
        os.utime(path, None)

# ----------------------------------------------------------------------------------------------------
#
#                                      generate file name
#
# ----------------------------------------------------------------------------------------------------
# Create a full path file name from the directory and the file name
#   only here as we have multiple OS to work with.


def file_generate_name(p_dir, p_file):
    """
    create filename with respect to OS considerations.
    """

    lp.log_debug('start gen_filename')
    return p_dir + DIR_SEPARATOR + p_file

# ----------------------------------------------------------------------------------------------------
#
#                                 Return Date Time string for filename
#
# ----------------------------------------------------------------------------------------------------

def now():
    """
    Return Date_Time as a string %Y%m%d_%H%M%S
    """
    return time.strftime("%Y%m%d_%H%M%S")

# ----------------------------------------------------------------------------------------------------
#
#                          Return Date Time with MS string for filename
#
# ----------------------------------------------------------------------------------------------------


def now_with_ms():
    """
    Return Date_Time as a string %Y%m%d_%H%M%S_ms
    """

    curr = datetime.now()
    microsec = curr.microsecond
    return '{}_{}'.format(time.strftime("%Y%m%d_%H%M%S"), microsec)

# ----------------------------------------------------------------------------------------------------
#
#                                          Remove Dir
#
# ----------------------------------------------------------------------------------------------------


def dir_remove(p_dir):
    """
    remove directory
    Assumes directory is empty
    Full path name required.
    """
    lp.log_debug('start remove_dir')

    if os.path.isdir(p_dir):

        try:
            os.rmdir(p_dir)

        except OSError as err:
            print("\nFailed to remove directory :{0}, aborting\n")
            print("OS Error({0}): {1}".format(err.errno, err.strerror))
            print("\n")
            exit(2)

# ----------------------------------------------------------------------------------------------------
#
#                                         fetch Work Dir
#
# ----------------------------------------------------------------------------------------------------


def dir_fetch_workdir():
    """
    Fetch the current working directory
    """
    lp.log_debug('start fetchwork_dir')
    if lp.IS_WINDOWS:
        work_dir = os.environ['USERPROFILE'] + '/log'
        work_dir = work_dir.replace('\\', '/')
    else:
        work_dir = os.environ['HOME'] + '/log'

    return work_dir

# ----------------------------------------------------------------------------------------------------
#
#                                                 Create Dir
#
# ----------------------------------------------------------------------------------------------------


def dir_create(p_dir):
    """
    Create Directory
    """
    lp.log_debug('start create_dir')

    if os.path.isdir(p_dir):
        return True
    else:
        try:
            os.makedirs(p_dir)

        except OSError as err:
            lp.log_warning("\nFailed to create directory :{0}, aborting\n")
            lp.log_warning("OS Error({0}): {1}".format(err.errno, err.strerror))
            lp.log_warning("\n")
            return False

    return True

# ----------------------------------------------------------------------------------------------------
#
#                          Determine log filename
#
# ----------------------------------------------------------------------------------------------------


def log_filename_determine(p_work_dir, p_program):
    """
    Fetch log file name
    """
    lp.log_debug('start log_filename_determine')

    # Get the time in milliseconds
    curr = datetime.datetime.now()
    debug_microsec = curr.microsecond

    debug_datetime = time.strftime("%Y%m%d_%H%M%S")

    log_file_template = '{vwDir}/{vProg}_{vDT}_{vMS}.log'

    log_file = log_file_template.format(vwDir=p_work_dir,
                                        vProg=p_program,
                                        vDT=debug_datetime,
                                        vMS=debug_microsec)
    return log_file

# ----------------------------------------------------------------------------------------------------
#
#                          init log file
#
# ----------------------------------------------------------------------------------------------------


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

    if over_ride_name is None:
        program_name = sys.argv[0]
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

# --- eof ---
