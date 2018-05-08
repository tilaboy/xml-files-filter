import sys
import xml.etree.ElementTree as ET
import os
import re

class trxml():
    def __init__(self, trxml_file=None):
        self.trxml_file = trxml_file

        self.size = os.path.getsize(trxml_file)
        print('creating a new trxml object from {}'.format(self.trxml_file))

        with open(trxml_file, 'r') as f:
            trxml_string = f.read()
            self.trxml_string = trxml_string
            # print(trxml_string)

        try:
            tree = ET.parse(trxml_file)
            root = tree.getroot()

            print ('found root {}'.format(root.tag))
            self.topLevelTag = root.tag
            self.ExtractionPart = root.find('Document')
            self.DerivedPart = root.find('DocumentStructure')
        except Exception as e:
            print("ERROR: parse failed\n")
            print(e)

        try:
            xpath = "ItemGroup[@key='{}']/Item[{}]/Field[@key='{}']/Value".format('address', '1', 'countrycode_nodefault')
            print ("xpath :{}".format(xpath))
            self.country = self.DerivedPart.find(xpath).text
            print(self.country)
        except Exception as e:
            print("ERROR: country parsing failed\n")
            print(e)


        return

    def get_account (self):
        return self.ExtractionPart.get('account')

    def get_lang(self):
        return self.ExtractionPart.get('lang')

    def get_size(self):
        return int(self.size / 1024)

    def get_orig_filetype(self):
        mime_type = self.ExtractionPart.get('content_type')
        return re.sub('^.*/', '' , mime_type)

    def get_pathtype(self):
        file_type = self.ExtractionPart.get('path', default='standard')
        return file_type

    def get_country(self):
        return self.country
