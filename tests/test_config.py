import os
import re
import tempfile
import json
from unittest import TestCase

from xml_filter.config import Config

class ConfigTestCases (TestCase):
    'unit tests for config files'
    def setUp(self):
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
        
        tmp_wrong = tempfile.NamedTemporaryFile()
        self.wrong_config_filename = tmp_wrong.name
        with open(self.wrong_config_filename, 'w') as fp_wrong:
            json.dump(wrong_config, fp_wrong)
        
        



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
        tmp_correct = tempfile.NamedTemporaryFile()
        self.correct_config_filename = tmp_correct.name
        with open(self.correct_config_filename, 'w') as fp_correct:
            json.dump(right_config, fp_correct)
        config = Config(self.correct_config_filename)
        assert config.get('nr_docs') == 2000
        fp_correct.close()
