import sys
import xml.etree.ElementTree as ET
import os
import re

class trxml():
    def __init__(self, trxml_file=None):
        self.trxml_file = trxml_file
        
        self.size = os.path.getsize(trxml_file)
        print('create a new trxml object from {}'.format(self.trxml_file))

        with open(trxml_file, 'r') as f:
            trxml_string = f.read()
            self.trxml_string = trxml_string
            print(trxml_string)

        try:
            tree = ET.parse(trxml_file)
            root = tree.getroot()
            print ('found root {}'.format(root.tag))
            self.topLevelTag = root.tag
            self.topLevelObj = root

        except Exception as e:
            print("ERROR: parse failed\n")
            print(e)
        return

    def get_lang(self):
        return self.topLevelObj.get('lang')

    def get_size(self):
        return self.size

    def get_orig_filetype(self):
        mime_type = self.topLevelObj.get('content_type')
        return re.sub('application/', '' , mime_type)

    def get_pathtype(self):
        file_type = self.topLevelObj.get('path', default='standard') 
        return file_type
