import sys
import xml.etree.ElementTree as ET
import os
import re

from xml_filter.xml import Xml

class Trxml(Xml):

    def get_orig_filename(self):
        return re.sub("\.trxml", "", self.input_filename)
