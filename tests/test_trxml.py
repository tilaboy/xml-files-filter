import os
import re

from unittest import TestCase
from xml_filter.trxml import Trxml

class TrxmlTestCases (TestCase):
    'unit tests for trxml object'
    def setUp(self):
        local_dir = 'tests/resource'
        trxml_file = os.path.join(local_dir, 'test.trxml')
        self.trxml_obj = Trxml(trxml_file)

    def test_trxml_filename(self):
        '''Test: test the filename, original filename, filesize'''
        assert self.trxml_obj.file_size == 3, 'get file size'
        assert self.trxml_obj.input_filename == 'test.trxml', 'get filename'
        assert self.trxml_obj.orig_filename == 'test', 'get original filename'

    def test_working_trxml_tag(self):
        '''Test: test the selection of the working tag'''
        document_xml_obj = self.trxml_obj.get_working_entity('Document')
        assert document_xml_obj.tag == 'Document', 'get top level tag'
        document_structure_xml_obj = self.trxml_obj.get_working_entity('DocumentStructure')
        assert document_structure_xml_obj.tag == 'DocumentStructure', 'get top level tag'


    def test_trxml_attributes(self):
        '''TEST: check whether function get the correct xml attributes'''
        working_trxml_obj = self.trxml_obj.get_working_entity('Document')
        assert working_trxml_obj.get('account') == 'abcdefg',\
        'attribute: account'
        assert working_trxml_obj.get('lang') == 'english',\
        'attribute: language'
        assert working_trxml_obj.get('path', default='standard') == 'standard',\
        'attribute: path'
        assert re.search('pdf', working_trxml_obj.get('content_type')),\
         'attribute: type'

    def test_trxml_field_selector(self):
        '''Test: select the field and retrieve the value of that field'''
        working_trxml_obj = self.trxml_obj.get_working_entity('DocumentStructure')
        xpath_country = "ItemGroup[@key='{}']/Item[@index='{}']/Field[@key='{}']/Value".\
        format('address', '0', 'countrycode_nodefault')
        assert working_trxml_obj.find(xpath_country).text == 'US'

        xpath_model = "ItemGroup[@key='{}']/Item[@index='{}']/Field[@key='{}']/Value".\
        format('__MODEL_VERSION__', '0', 'Textractor')
        assert working_trxml_obj.find(xpath_model).text == '4.1.DEV'
