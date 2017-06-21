"""
Send Email
"""
from __future__ import division

import os
import re
# import string
# import logging
# import time
import argparse
import smtplib
import getpass
import socket
import mimetypes
# import cx_Oracle

import home_lib as hlib

# from utilities import  *

# ------------------------------
# Doc for email lib: https://docs.python.org/3.3/library/email.mime.html
#    different for python 2.2

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage

# ------------------------------------------------------------------------------
#
#                                 VALIDATE MAIL TO
#
# ------------------------------------------------------------------------------


def validate_mail_to(mystr):
    """ Validate the target email address """

    print("mail to {}".format(mystr))
    # mail_to is mandatory, so check length
    if len(mystr) < 4:
        hlib.p_e("ERROR: Mail to address is invalid, must be greater than 4 characters in length")
        hlib.p_e("       Email address supplied [{}]".format(mystr))
        return False

    # Validate that email address contains a @
    if re.search('@', mystr):
        pass
    else:
        hlib.p_e("ERROR: Mail to address is invalid")
        hlib.p_e("       must contain '@'. Email address supplied [{}]".format(mystr))
        return False

    return


# ------------------------------------------------------------------------------
#
#                                 VALIDATE MAIL FROM
#
# ------------------------------------------------------------------------------


#def validate_mail_from(mystr):
#    """ Generate Mail From address """
#
#    l_user = getpass.getuser()
#    l_host = socket.gethostbyaddr(socket.gethostname())[0]
#
#    # Check for null mail from
#    if not mystr:
#        mystr = '{}@{}'.format(l_user, l_host)
#
#    # Validate that email address contains a @
#    if re.search('@', mystr):
#        pass
#    else:
#        hlib.p_e("ERROR: from address is invalid")
#        hlib.p_e("       must contain '@'. Email address supplied [{}]".format(mystr))
#        mystr = None
#
#    return mystr

# ------------------------------------------------------------------------------
#
#                                 Attach File
#
# ------------------------------------------------------------------------------


def attach_file(p_attach, p_outer):
    """ Attach the file with the correct file type """

    if p_attach is not None:

        ctype, encoding = mimetypes.guess_type(p_attach)
        # print ("ctype : %s, encoding : %s" % (ctype, encoding))

        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
            subtype = 'plain'

        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            l_file = open(p_attach)
            # Note: we should handle calculating the charset
            l_att = MIMEText(l_file.read(), _subtype=subtype)
            l_file.close()
        elif maintype == 'image':
            l_file = open(p_attach, 'rb')
            l_att = MIMEImage(l_file.read(), _subtype=subtype)
            l_file.close()
        elif maintype == 'audio':
            l_file = open(p_attach, 'rb')
            l_att = MIMEAudio(l_file.read(), _subtype=subtype)
            l_file.close()
        elif maintype == 'application':
            l_file = open(p_attach, 'rb')
            l_att = MIMEApplication(l_file.read(), _subtype=subtype)
            l_file.close()
        else:
            l_file = open(p_attach, 'rt')
            l_att = MIMEText(maintype, subtype)
            l_att.set_payload(l_file.read())
            l_file.close()

        # Set the filename parameter
        l_basename = os.path.basename(p_attach)
        l_att.add_header('Content-Disposition', 'attachment', filename=l_basename)
        p_outer.attach(l_att)


# ------------------------------------------------------------------------------
#
#                                 SEND MAIL
#
# ------------------------------------------------------------------------------


def sendmail_internal(p_email_config, p_to, p_subject, p_attach, p_attach2, p_inline):
    """ Send email internal (do not use the OS interface) """
    hlib.log_debug('Start sendmail_internal')
    outer = MIMEMultipart()

    if p_inline is not None:
        hlib.log_debug('    p_inline is not None')
        p_args_inline = p_inline.replace('\\', '/')

        msg = MIMEMultipart('alternative')
        print(p_args_inline)
        if re.search('.html', p_args_inline):
            hlib.log_debug('        inline html')
            subtype = 'html'
        else:
            hlib.log_debug('        inline plain')
            subtype = 'plain'

            # ctype, encoding = mimetypes.guess_type(my_args['attach'])

        # print "ctype : %s, encoding : %s" % (ctype, encoding)
        l_file = open(p_args_inline, 'rb')
        msg = MIMEText(l_file.read(), subtype, _charset='utf-8')
        l_file.close()

        outer.attach(msg)

    if p_attach is not None:
        hlib.log_debug('    p_attach is not None')
        attach_file(p_attach, outer)

    if p_attach2 is not None:
        hlib.log_debug('    p_attach2 is not None')
        attach_file(p_attach2, outer)

    default_me = p_email_config['from']
    default_you = p_email_config['to']
    passwd = p_email_config['pass']

    if p_to is None:
        l_to = default_you
    else:
        l_to = p_to

    outer['Subject'] = p_subject
    outer['From'] = default_me
    outer['To'] = l_to

    rec = []
    for j in p_to.split(','):
        rec.append(j)

    hlib.log_debug('    start comms')

#    l_comms = smtplib.SMTP('smtpmail.racqgroup.local')
#    l_comms.sendmail(p_from, rec, outer.as_string())
#    l_comms.quit()

    s = smtplib.SMTP("smtp.live.com", 587)
    s.ehlo()                     # Hostname to send for this command defaults to the fully
                                 # qualified domain name of the local host.
    s.starttls()                 # Puts connection to SMTP server in TLS mode
    s.ehlo()
    s.login(default_me, passwd)

    s.sendmail(default_me, l_to, outer.as_string())

    s.quit()

    return

# ------------------------------------------------------------------------------
#
#                                 Initialise
#
# ------------------------------------------------------------------------------


def initialise():
    """
    Necessary initialisations for command line arguments
    """
    # Logfile for logging
    log_filename = hlib.log_filename_init()
    if log_filename is None:
        print("\nError: Failed to initialise Log File Name. aborting\n")
        return -1

    parser = argparse.ArgumentParser(description="""
    send mail!
    """, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-s', '--subject',
                        help='Add a subject line to the email',
                        required=True)

    parser.add_argument('-f', '--from',
                        help='From email address',
                        required=True)

    parser.add_argument('-t', '--to',
                        help='To email address (comma seperated list)',
                        required=True)

    parser.add_argument('-a', '--attach',
                        help='add attachment (full path required)',
                        required=False)

    parser.add_argument('-b', '--attach2',
                        help='add 2nd attachment (full pathrequired)',
                        required=False)

    parser.add_argument('-i', '--inline',
                        help='body/text of email (full path required)',
                        required=False)

    # Add arguments
    parser.add_argument('-d', '--debug',
                        help='Log messages verbosity: NONE (least), DEBUG (most)',
                        choices=('NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'),
                        default="INFO",
                        required=False)

    # Sort though the arguments, ensure mandatory are populated
    args = hlib.args_validate(parser, log_filename)
    return args


# ------------------------------------------------------------------------------
#
#                                 process
#
# ------------------------------------------------------------------------------

def send_email(p_to,
               p_subject=None,
               p_attach=None,
               p_attach2=None,
               p_inline=None):
    """ This interface is where other programs access email from """

    email_config = hlib.init_email()
    if email_config is None:
        print('Failed to init email, aborting')
        return hlib.FAIL_GENERIC

    if validate_mail_to(p_to) is not None:
        return False

    if p_attach is not None:
        if not os.path.isfile(p_attach):
            print('\nWARNING: File [%s] does not exist. Sending email anyway\n' % (p_attach))
            p_attach = None

    if p_inline is not None:
        if not os.path.isfile(p_inline):
            print('\nWARNING: File [%s] does not exist. Sending email anyway\n' % (p_inline))
            p_inline = None
    p_subject += ' Run by:{} on {}'.format(os.getlogin(), socket.gethostname())
    hlib.log_debug('Call sendmail_internal')

    sendmail_internal(email_config, p_to, p_subject, p_attach, p_attach2, p_inline)

    hlib.log_debug('end sendmail_internal')

    return True

# ------------------------------------------------------------------------------
#
#                                 MAIN
#
# ------------------------------------------------------------------------------


def main():
    """ OS Interface for sending email"""

    args = initialise()

    p_from = args['from']
    p_to = args['to']
    p_subject = args['subject']
    p_attach = args['attach']
    p_attach2 = args['attach2']
    p_inline = args['inline']

    send_email(p_from, p_to, p_subject, p_attach, p_attach2, p_inline)

    return hlib.SUCCESS

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    retval = main()
    if retval == hlib.SUCCESS:
        exit
    else:
        exit(retval)

# --- eof ---
