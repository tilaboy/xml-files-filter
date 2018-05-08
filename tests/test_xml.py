import os

from unittest import TestCase
from xmlfilter.xml import xml

class XmlTestCases (TestCase):
    'unit tests for xml object'
    def setUp(self):
        local_dir = 'tests/resource'
        xml_file = os.path.join(local_dir, 'test.xml')
        self.xmlObj = xml(xml_file)

    def test_xml_account(self):
        lang = self.xmlObj.get_account()
        assert lang == 'davinci'

    def test_xml_lang(self):
        lang = self.xmlObj.get_lang()
        assert lang == 'english'

    def test_xml_size(self):
        size = self.xmlObj.get_size()
        assert size == 3

    def test_xml_pathtype(self):
        pathtype = self.xmlObj.get_pathtype()
        assert pathtype == 'standard'


    def test_xml_orig_filetype(self):
        orig_filetype = self.xmlObj.get_orig_filetype()
        assert orig_filetype == 'pdf'
