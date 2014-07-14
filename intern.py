import os, sys, csv, time
from email.utils import parsedate
from datetime import datetime
from pytz import timezone
import logging
from logging import handlers

logger = logging.getLogger()
# Change logging level here (CRITICAL, ERROR, WARNING, INFO or DEBUG)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Logging variables
MAX_BYTES = 200000
# Max number appended to log files when MAX_BYTES reached
BACKUP_COUNT = 5
log_file = sys.argv[2]

fh = logging.handlers.RotatingFileHandler(log_file,
                                          'a',
                                          MAX_BYTES,
                                          BACKUP_COUNT)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# Log to the console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

def make_call(client, phone_no, from_no, callback_url):
    """
    Uses the Twilio API to make the call to the REST service

    Args:
        client: an instance of the TwilioRestClient
        phone_no: the phone number to call
        from_no: the phone number to call from (show's up in the
            receiptent's call ID)
        callback_url: the REST endpoint that the intern will make a call to

    """
    call = client.calls.create(to=phone_no,
                               from_=from_no,
                               url=callback_url)
    return call.sid

def make_calls(csv_file):
    """
    Iterates over the call list and makes a call for each phone number.

    Args:
        csv_file: A comma-separated file of phone numbers to call
            in the first column
    """
    from_no = os.environ['INTERN_FROM']
    callback_url = os.environ['INTERN_URL'] + '/intro'
    account = os.environ['INTERN_ACCT']
    token = os.environ['INTERN_TOKEN']
    call_delay = int(os.environ['CALL_DELAY'])

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient(account, token)

    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        logger.info('Ok, intern\'s ready to make the calls...')
        for row in reader:
            try:
                call_sid = make_call(client, row[0], from_no, callback_url)
                logger.info('The intern made a call to {0}:{1}'.format(row[0], call_sid))
            except Exception as err:
                logger.error(err)
                logger.info('Continuing...')
            logger.debug('Waiting for ' + str(call_delay / 60) + ' minutes before the next call...')
            time.sleep(call_delay)
        logger.info('The electronic intern is done! Time to check Reddit.')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'You forgot to give the intern a CSV of phone numbers and a log file to write to!'
    else:
        make_calls(sys.argv[1])