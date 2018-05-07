from unittest import TestCase, mock
from xmlfilter import xml

class xmlTestCases (TestCase):
    def setup(self):
        input_xml_string = '<begin lang="english">english documents</begin>'
        xml_obj = xml(input_xml_string)

    def test_xml_lang(self):
        lang = self.xml_obj.get_lang()
        
