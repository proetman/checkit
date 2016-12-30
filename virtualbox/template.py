"""
This is a template for all new programs
"""

from __future__ import division
from __future__ import print_function

# Import OS Functions
import argparse
# import datetime
# import math

# Import racq library for RedShift
# import pandas as pd
import lib_proj as lp
import lib_file as lfile

# ----------------------------------------------------------------------------------------------------
#
#                                             Constants
#
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
#
#                                             Initialize
#
# ----------------------------------------------------------------------------------------------------


def initialise():
    """
    Process all command line arguments.
    handle any mandatory stuff.
    handle any mutually exclusive parameters, etc.
    return dict with all arguments.

    Note: If logfile name needs to contain parameter, this is handled here as well!
    """

    # Logfile for logging
    log_filename = lfile.log_filename_init()
    if log_filename is None:
        print("\nError: Failed to initialise Log File Name. aborting\n")
        return -1
    # parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="""
        Example command lines:

        -d DEBUG -t my_table_name
          """, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-t', '--table',
                        help='Enter table name',
                        required=True)

    # Add arguments
    parser.add_argument('-d', '--debug',
                        help='Log messages verbosity: NONE (least), DEBUG (most)',
                        choices=('NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'),
                        default="INFO",
                        required=False)

    # Sort though the arguments, ensure mandatory are populated
    args = lp.args_validate(parser, log_filename)
    return args


# ----------------------------------------------------------------------------------------------------
#
#                                             Main
#
# ----------------------------------------------------------------------------------------------------

def main():
    """"
    Main process.
        Handle argument parsing.
        Setup connections.
        Call main process.
        Return status.
    """

    args = initialise()

    p_table = args['table']
    print("My table name is '{}'.".format(p_table))

    if p_table is None:
        return lp.FAIL
    else:
        return lp.SUCCESS

# ----------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    if main() == lp.SUCCESS:
        exit()
    else:
        exit(1)

# --- eof ---
