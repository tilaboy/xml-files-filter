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
                raise(error)
        self.config = config

        self.config_validation()

    def config_validation(self):
        pass
