import os
from flask import Flask, make_response, request
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
env = Environment(autoescape=True,
                  loader=FileSystemLoader(os.path.join(
                    os.path.realpath(os.path.dirname(__file__)),
                    'twiml')))
app.debug = False

@app.route('/intro', methods=['GET', 'POST'])
def intro():
    """Play the intro message."""
    resp_xml = env.get_template('intro.xml')
    resp = make_response(resp_xml.render())
    resp.headers['Content-Type'] = 'application/xml'
    return resp

@app.route('/forward', methods=['GET'])
def forward():
    """Listen for a keypress of 4, if so, forward call to PhillyASAP office"""
    digit = request.values.get('Digits', None)
    if digit == '4':
        resp_xml = env.get_template('forward.xml')
        forward_no = os.environ['PHILLYASAP_FORWARD_NO']
        resp = make_response(resp_xml.render(forward_no=forward_no))
        resp.headers['Content-Type'] = 'application/xml'
        return resp
    elif digit == '1':
        resp_xml = env.get_template('repeat.xml')
        resp = make_response(resp_xml.render())
        resp.headers['Content-Type'] = 'application/xml'
        return resp
    else:
        resp_xml = env.get_template('correct.xml')
        resp = make_response(resp_xml.render())
        resp.headers['Content-Type'] = 'application/xml'
        return resp

if __name__ == '__main__':
    app.run(port=8000)