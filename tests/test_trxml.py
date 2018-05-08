import os

from unittest import TestCase
from xmlfilter.TKtrxml import TKtrxml

class TrxmlTestCases (TestCase):
    'unit tests for trxml object'
    def setUp(self):
        local_dir = 'tests/resource'
        trxml_file = os.path.join(local_dir, 'test.trxml')
        self.trxmlObj = TKtrxml(trxml_file)

    def test_xml_account(self):
        lang = self.trxmlObj.get_account()
        assert lang == 'derwentexec_cv'

    def test_trxml_lang(self):
        lang = self.trxmlObj.get_lang()
        print("test language: {}".format(lang))
        assert lang == 'english'

    def test_trxml_size(self):
        size = self.trxmlObj.get_size()
        print("test file size: {}".format(size))
        assert size == 205

    def test_trxml_pathtype(self):
        pathtype = self.trxmlObj.get_pathtype()
        print("test file path: {}".format(pathtype))
        assert pathtype == 'standard'


    def test_trxml_orig_filetype(self):
        orig_filetype = self.trxmlObj.get_orig_filetype()
        print("test file mimetype: {}".format(orig_filetype))
        assert orig_filetype == 'xml'

    def test_trxml_country (self):
        country = self.trxmlObj.get_country()
        assert country == 'US'
