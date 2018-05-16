import sys
import os
import re
import json

class Config():
    def __init__(self, config_file=''):
        config = {}
        with open(config_file, 'r') as config_fh:
            try:
                config.update(json.load(config_fh))
            except Exception as error:
                print("ERROR: parse failed\n")
                raise RuntimeError(error)
        self.config = config
        self.config_validation()

    def config_validation(self):
        if self.config.get('input_type') == 'xml' and self.config.get('field_selectors'):
            raise AttributeError('ERROR: Config issue.\n\
            field_selector is defined for xml, but it is only valid for trxml')

        if self.config.get('max_per_account') and not self.config.get('nr_docs'):
            raise AttributeError('ERROR: Config issue.\n\
            field_selector is defined for xml, but it is only valid for trxml')
