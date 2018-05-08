import sys
import xml.etree.ElementTree as ET
import os
import re

class xml():
    def __init__(self, xml_file=None):
        self.xml_file = xml_file

        self.size = os.path.getsize(xml_file)
        print('create a new xml object from {}'.format(self.xml_file))

        with open(xml_file, 'r') as f:
            xml_string = f.read()
            self.xml_string = xml_string

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            print ('found root {}'.format(root.tag))
            self.topLevelTag = root.tag
            self.topLevelObj = root

        except Exception as e:
            print("ERROR: parse failed\n")
            print(e)
        return

    def get_account (self):
        return self.topLevelObj.get('account')

    def get_lang(self):
        return self.topLevelObj.get('lang')

    def get_size(self):
        return int(self.size / 1024)

    def get_orig_filetype(self):
        mime_type = self.topLevelObj.get('content_type')
        return re.sub('^.*/', '' , mime_type)

    def get_pathtype(self):
        file_type = self.topLevelObj.get('path', default='standard')
        return file_type
