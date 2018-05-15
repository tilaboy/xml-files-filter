import os
import re

from unittest import TestCase
from xml_filter.xml import Xml

class XmlTestCases (TestCase):
    'unit tests for xml object'
    def setUp(self):
        local_dir = 'tests/resource'
        xml_file = os.path.join(local_dir, 'test.xml')
        self.xml_obj = Xml(xml_file)

    def test_xml_file(self):
        '''Test: test the filename, original filename, filesize'''
        assert self.xml_obj.file_size == 0, 'get file size'
        assert self.xml_obj.input_filename == 'test.xml', 'get filename'
        assert self.xml_obj.orig_filename == 'test', 'get original filename'

    def test_working_xml_tag(self):
        '''Test: test the selection of the working tag'''
        working_xml_obj = self.xml_obj.get_working_entity('begin')
        assert working_xml_obj.tag == 'begin', 'get top level tag'

    def test_xml_attributes(self):
        '''TEST: check whether function get the correct xml attributes'''
        working_xml_obj = self.xml_obj.get_working_entity('begin')
        assert working_xml_obj.get('account') == 'abcdefg',\
        'attribute: account'
        assert working_xml_obj.get('lang') == 'english',\
        'attribute: language'
        assert working_xml_obj.get('path', default='standard') == 'standard',\
        'attribute: path'
        assert re.search('pdf', working_xml_obj.get('content_type')),\
         'attribute: type'
