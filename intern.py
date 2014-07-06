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
log_file = 'log.txt'

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

def log_results(client, results):
    """
    Logs the results of the intern's calls to a CSV file by calling Twilio's
    API for details of each call made by the intern.

    Args:
        client: an instance of the TwilioRestClient
        results: an array of IDs (SIDs) for the calls made by the intern
            in this session

    """
    with open('call_lists/results_' + str(int(time.time())) + '.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['DATE', 'START_TIME', 'END_TIME', 'TO', \
                         'DURATION (SEC)', 'RESULT', 'SID', 'COST (CENTS)'])
        est = timezone('US/Eastern')
        for result in results:
            call = client.calls.get(result)
            while call.status == 'in-progress' or call.status == 'ringing':
                logger.debug('Call\'s still going on...')
                time.sleep(30)
                call = client.calls.get(result)
            else:
                start = parsedate(call.start_time)
                start = datetime(*start[:6], microsecond=0)
                start_est = est.localize(start)
                end = parsedate(call.end_time)
                end = datetime(*end[:6], microsecond=0)
                end_est = est.localize(end)
                writer.writerow([start_est.strftime('%m/%d/%y'),
                                 start_est.strftime('%H:%M %p'),
                                 end_est.strftime('%m/%d/%y'),
                                 call.to[2:],
                                 call.duration,
                                 call.status,
                                 call.sid,
                                 round(float(call.price), 3)])
    return True

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

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient(account, token)

    call_results = []

    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        logger.info('Ok, intern\'s ready to make the calls...')
        for row in reader:
            call_sid = make_call(client, row[0], from_no, callback_url)
            logger.info('The intern made a call to {0}:{1}'.format(row[0], call_sid))
            call_results.append(call_sid)
            time.sleep(45)

    logger.debug('The intern is logging the calls results...')
    intern_logging = log_results(client, call_results)
    if intern_logging:
        logger.info('The electronic intern is done! Time to check Reddit.')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'You forgot to give the intern a CSV of phone numbers!'
    else:
        make_calls(sys.argv[1])