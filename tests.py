import unittest, requests, os
import xml.etree.ElementTree as ET

class TestCase(unittest.TestCase):
    def test_intro_message(self):
        r = requests.get('http://localhost:8000/intro')
        root = ET.fromstring(r.content)
        assert root[0].tag == 'Gather'
        assert root[0][0].tag == 'Say'
        assert root[0].attrib['action'] == '/forward'
        assert root[0].attrib['method'] == 'GET'
        assert r.headers['content-type'] == 'application/xml'

    def test_forward_correct_digit(self):
        r = requests.get('http://localhost:8000/forward?Digits=1')
        root = ET.fromstring(r.content)
        assert root[0].tag == 'Say'
        assert root[1].tag == 'Dial'
        assert root[1].text == os.environ['PHILLYASAP_FORWARD_NO']

    def test_repeat(self):
        r = requests.get('http://localhost:8000/forward?Digits=4')
        root = ET.fromstring(r.content)
        assert root[0].tag == 'Gather'
        assert root[0][0].tag == 'Say'
        assert root[0].attrib['action'] == '/forward'
        assert root[0].attrib['method'] == 'GET'
        assert r.headers['content-type'] == 'application/xml'

    def test_forward_incorrect_digit(self):
        r = requests.get('http://localhost:8000/forward?Digits=5')
        root = ET.fromstring(r.content)
        assert root[0].tag == 'Gather'
        assert root[1].tag == 'Say'

if __name__ == '__main__':
    unittest.main()