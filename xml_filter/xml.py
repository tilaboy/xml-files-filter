import sys
import xml.etree.ElementTree as ET
import os
import re

class Xml():
    def __init__(self, xml_file=None):
        self.input_filename = os.path.basename(xml_file)
        self.orig_filename = self.get_orig_filename()

        print('create a new xml object from {}'.format(self.input_filename))

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            assert re.match('begin|TextractorResult', root.tag), 'The topLevelTag is not begin'

            self.top_level_tag = root.tag
            self.top_level_obj = root

        except Exception as e:
            print("ERROR: parse failed\n")
            raise(e)
        else:
            pass

        self.file_size = int ( os.path.getsize(xml_file) / 1024 )


    def get_orig_filename(self):
        return re.sub("\.xml", "", self.input_filename)

    def get_working_entity(self, working_tag=''):
        working_xml_obj = None
        print ('searching for tag {}'.format(working_tag))
        if self.top_level_tag == working_tag:
            working_xml_obj = self.top_level_obj
        else:
            working_xml_obj = self.top_level_obj.find(working_tag)

        if working_xml_obj is None:
            raise ("ERROR: {} not found in input doc {}".format(self.input_filename))

        # print ('test attribute lang: {}'.format(working_xml_obj))
        return working_xml_obj
