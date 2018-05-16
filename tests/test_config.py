import os
import re
import tempfile
import json
from unittest import TestCase

from xml_filter.config import Config

class ConfigTestCases (TestCase):
    'unit tests for config files'

    def test_correct_config(self):
        '''Test: test reading a correct config file'''
        right_config = {
            "input_type": "trxml",
            "nr_docs": 2000,
            "attribute_filters": {
                "Document": {
                    "lang": { "value":"english" },
                    "content_type": { "value":["application/pdf", "application/msword"]},
                    "path": { "value": "standard", "default": "standard"}
                }
            },
            "field_selectors": {
                "DocumentStructure": {
                    "country": {
                        "xpath":"foo/bar",
                        "value":"US"
                    }
                }
            },
            "min_size": 800,
            "max_per_account": 0.1
        }
        tmp_file = tempfile.NamedTemporaryFile()
        self.config_filename = tmp_file.name
        with open(self.config_filename, 'w') as fh:
            json.dump(right_config, fh)
        try:
            config_class = Config(self.config_filename)
        except Exception as Error:
            raise "ERROR: could not load the correct config file\n"
        assert config_class.config['input_type'] == 'trxml'
        assert config_class.config['nr_docs'] == 2000
        assert config_class.config['min_size'] == 800
        fh.close()

    def test_wrong_config(self):
        '''Test: test reading a wrong config file'''
        wrong_config = {
            "input_type": "xml",
            "nr_docs": 2000,
            "field_selectors": {
                "DocumentStructure": {
                    "country": {
                        "xpath":"foo/bar",
                        "value":"US"
                    }
                }
            },
            "min_size": 800,
            "max_per_account": 0.1
        }
        tmp_file= tempfile.NamedTemporaryFile()
        self.config_filename = tmp_file.name
        with open(self.config_filename, 'w') as fh:
            json.dump(wrong_config, fh)

        try:
            config_class = Config(self.config_filename)
        except Exception as Error:
            assert str(Error).find('field_selector is defined for xml') > 0
        fh.close()
