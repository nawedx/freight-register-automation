import time, sys
#sys.stdout = open('runlog.txt', 'w')

import invoice_details_download
time.sleep(3)

import message_generator

import send_mail_position

'''
TODO

1. Automated logging of all errors and stdouts to a file and reproting of it to me in case of failure.
2. Checking for failure of message generation and restarting mechanism in case of failure.

'''