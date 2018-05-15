import sys
import xml.etree.ElementTree as ET
import os
import re

class Xml():
    '''xml class:
    xml tree object generated from xml file
    '''
    def __init__(self, xml_file=None):
        self.input_filename = os.path.basename(xml_file)
        self.orig_filename = self.get_orig_filename()

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            self.top_level_tag = root.tag
            self.top_level_obj = root

        except Exception as error:
            print("ERROR: parse xml file {} failed".format(xml_file))
            raise(error)
        else:
            pass

    def get_customer_account(self):
        return self.top_level_obj.get('account')

    def get_orig_filename(self):
        return re.sub("\.xml", "", self.input_filename)

    def get_working_entity(self, working_tag=''):
        working_xml_obj = None

        if self.top_level_tag == working_tag:
            working_xml_obj = self.top_level_obj
        else:
            working_xml_obj = self.top_level_obj.find(working_tag)

        if working_xml_obj is None:
            raise ("ERROR: {} not found in input doc {}".format(working_tag, self.input_filename))

        return working_xml_obj
