import os

from unittest import TestCase
from xmlfilter.xml import trxml

class TrxmlTestCases (TestCase):
    'unit tests for trxml object'
    def setUp(self):
        local_dir = 'tests/resource'
        trxml_file = os.path.join(local_dir, 'test.trxml')
        self.trxmlObj = trxml(trxml_file)

    def test_trxml_lang(self):
        lang = self.trxmlObj.get_lang()
        assert lang == 'english'

    def test_trxml_size(self):
        size = self.trxmlObj.get_size()
        assert size == 3807

    def test_trxml_pathtype(self):
        pathtype = self.trxmlObj.get_pathtype()
        assert pathtype == 'standard'


    def test_trxml_orig_filetype(self):
        orig_filetype = self.trxmlObj.get_orig_filetype()
        assert orig_filetype == 'pdf'
