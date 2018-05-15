import sys
import xml.etree.ElementTree as ET
import os
import re

from xml_filter.xml import Xml

class Trxml(Xml):

    def get_orig_filename(self):
        return re.sub("\.trxml", "", self.input_filename)

    def get_customer_account(self):
        working_trxml_obj = self.trxml_obj.get_working_entity('Document')
        return working_trxml_obj.get('account')

    def get_country(self):
        working_trxml_obj = self.trxml_obj.get_working_entity('DocumentStructure')
        xpath_country = "ItemGroup[@key='{}']/Item[@index='{}']/Field[@key='{}']/Value".\
        format('address', '0', 'countrycode_nodefault')
        return working_trxml_obj.find(xpath_country).text
