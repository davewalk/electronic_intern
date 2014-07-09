import os
from flask import Flask, make_response, request, redirect, url_for
from jinja2 import Environment, FileSystemLoader
import pymongo
from datetime import datetime

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:
    conn = pymongo.Connection(MONGO_URL)
    db = conn[urlparse(MONGO_URL).path[1:]]
else:
    conn = pymongo.Connection('localhost', 27017)
    db = conn['intern']

app = Flask(__name__)
env = Environment(autoescape=True,
                  loader=FileSystemLoader(os.path.join(
                    os.path.realpath(os.path.dirname(__file__)),
                    'twiml')))
app.debug = False

@app.route('/intro', methods=['GET', 'POST'])
def intro():
    """Play the intro message."""

    db.responses.insert({"to": to, "what": "response", "date": datetime.now()})

    resp_xml = env.get_template('intro.xml')
    mp3_url = os.environ['MP3_URL']
    resp = make_response(resp_xml.render(mp3_url=mp3_url))
    resp.headers['Content-Type'] = 'application/xml'
    return resp

@app.route('/forward', methods=['GET'])
def forward():
    """
    Listen for a keypress:

        - If 1, forward call to PhillyASAP office
        - If 4, repeat the message.
    """
    digit = request.values.get('Digits', None)
    to = request.values.get('To', None)

    db.responses.insert({"to": to, "digit": int(digit), "date": datetime.now()})

    if digit == '1':
        resp_xml = env.get_template('forward.xml')
        forward_no = os.environ['PHILLYASAP_FORWARD_NO']
        resp = make_response(resp_xmlrrender(forward_no=forward_no))
        resp.headers['Content-Type'] = 'application/xml'
        return resp
    elif digit == '4':
        return redirect(url_for('intro'))
    else:
        resp_xml = env.get_template('correct.xml')
        resp = make_response(resp_xml.render())
        resp.headers['Content-Type'] = 'application/xml'
        return resp

if __name__ == '__main__':
    app.run(port=8000)