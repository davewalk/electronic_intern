import os, sys, csv, time
from email.utils import parsedate
from datetime import datetime
from pytz import timezone

def make_call(client, phone_no, from_no, callback_url):
    call = client.calls.create(to=phone_no,
                               from_=from_no,
                               url=callback_url)
    return call.sid

def log_results(client, results):
    with open('call_lists/results_' + str(int(time.time())) + '.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['DATE', 'START_TIME', 'END_TIME', 'TO', \
                         'DURATION (SEC)', 'RESULT', 'SID', 'COST (CENTS)'])
        est = timezone('US/Eastern')
        for result in results:
            call = client.calls.get(result)
            if call.end_time:
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
            else:
                print 'Call\'s still going on...'
                time.sleep(45)
    return True


def make_calls(csv_file):
    from_no = os.environ['INTERN_FROM']
    callback_url = os.environ['INTERN_URL']
    account = os.environ['INTERN_ACCT']
    token = os.environ['INTERN_TOKEN']

    from twilio.rest import TwilioRestClient

    client = TwilioRestClient(account, token)

    call_results = []

    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        print 'Ok, intern\'s ready to make the calls...'
        for row in reader:
            call_sid = make_call(client, row[0], from_no, callback_url)
            print 'The intern made a call to {0}:{1}'.format(row[0], call_sid)
            call_results.append(call_sid)
            time.sleep(45)

    print 'The intern is logging the calls results...'
    intern_logging = log_results(client, call_results)
    if intern_logging:
        print 'The electronic intern is done! Time to check Reddit.'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'You forgot to give the intern a CSV of phone numbers!'
    else:
        make_calls(sys.argv[1])