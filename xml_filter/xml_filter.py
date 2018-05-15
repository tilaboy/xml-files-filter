#!/usr/bin/env python

import sys
import argparse
from os import listdir
import os
from os.path import isfile, join
from random import shuffle

from xml_filter.xml import Xml
from xml_filter.trxml import Trxml
from xml_filter.config import Config


def validate_file(file_obj, config):
    valid = 1
    for work_entity_tag, filters in config[attribute_filters].items():
        print ('work entity tag: {}'.format(work_entity_tag))
        working_entity = file_obj.get_working_entity(work_entity_tag)
        if not validate_field(working_entity, filters):
            valid = 0
            break

    return valid

def validate_field(working_entity, filters):
    valid = 1
    for attribute_name, attribute_value in filters.items():
        print('check {} for value {}'.format(attribute_name, attribute_value))
        if not working_entity.get(attribute_name) == attribute_value:
            valid = 0
            break

    return valid


def get_args():
    parser = argparse.ArgumentParser(description='read the list of xml or trxml\
    files, generate a list of documents which is a random subset fit the requirements')

    parser.add_argument('--config', help='config file to config the selectors', type=str)
    parser.add_argument('--input_dir', help='dir contains all xml or trxml to filter',\
     type=str)
    parser.add_argument('--output_file', help='type of the file to filter, xml or trxml',\
     type=str, default='select_filelist.txt')
    parser.add_argument('--filelist_to_skip', help='language to filter on', type=str)
    return parser.parse_args()

def get_files(input_dir):
    files = []
    for f in listdir(input_dir):
        if isfile(join(input_dir, f)):
            files.append(join(input_dir, f))
    return files

def get_file_obj(input_type, file_path):
    if input_type == 'xml':
        try:
            file_obj = Xml(file_path)
        except Exception as error:
            print("ERROR: not able to create xml object from {}".format(file_path))
            raise(e)

    if input_type == 'trxml':
        try:
            file_obj = Trxml(file_path)
        except Exception as error:
            print("ERROR: not able to create trxml object from {}".format(file_path))
            raise(e)

    return file_obj


def main(args):
    config = Config(args.config).config
    files = get_files(args.input_dir)
    shuffle(files)

    accounts = {}
    max_per_account = int(args.number * config[max_perc])
    output_fh = open(args.output_file,'w')
    for file_path in files:
        #print("checking file {}".format(file_path))
        file_obj = get_file_obj(config[input_type], file_path)
        is_valid_file = validate_file(file_obj, config)
        if is_valid_file:
            account = file_obj.get_customer_account()
            if accounts[account] < max_per_account:
                write(output_fh, file_path)
            else:
                pass
            accounts[account] = accounts[account] + 1

    close(output_fh)


if __name__ == '__main__':
    args = get_args()
    #TODO: country checking is not supported for xml
    main(args)
