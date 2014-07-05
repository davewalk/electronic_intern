import unittest, requests, os
import xml.etree.ElementTree as ET

class TestCase(unittest.TestCase):

    def setUp(self):
        if os.environ['PHILLYASAP_TEST_ENV'] == 'prod':
            self.uri = os.environ['INTERN_URL']
        else:
            self.uri = 'http://localhost:8000'

    def test_intro_message(self):
        r = requests.get(self.uri + '/intro')
        root = ET.fromstring(r.content)
        assert root[0].tag == 'Gather'
        assert root[0][0].tag == 'Play'
        assert root[0][0].text == os.environ['MP3_URL']
        assert root[0].attrib['action'] == '/forward'
        assert root[0].attrib['method'] == 'GET'
        assert r.headers['content-type'] == 'application/xml'

    def test_forward_correct_digit(self):
        r = requests.get(self.uri + '/forward?Digits=1')
        root = ET.fromstring(r.content)
        assert root[0].tag == 'Say'
        assert root[1].tag == 'Dial'
        assert root[1].text == os.environ['PHILLYASAP_FORWARD_NO']

    def test_repeat(self):
        r = requests.get(self.uri +'/forward?Digits=4')
        root = ET.fromstring(r.content)
        assert root[0].tag == 'Gather'
        assert root[0][0].tag == 'Play'
        assert root[0].attrib['action'] == '/forward'
        assert root[0].attrib['method'] == 'GET'
        assert r.headers['content-type'] == 'application/xml'

    def test_forward_incorrect_digit(self):
        r = requests.get(self.uri + '/forward?Digits=5')
        root = ET.fromstring(r.content)
        assert root[0].tag == 'Gather'
        assert root[0][0].tag == 'Say'

if __name__ == '__main__':
    unittest.main()