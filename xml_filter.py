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

    attribute_filters = config.get('attribute_filters', {})
    for work_entity_tag, filters in attribute_filters.items():
        working_entity = file_obj.get_working_entity(work_entity_tag)
        if not validate_attributes(working_entity, filters):
            return 0

    field_selectors = config.get('field_selectors', {})
    for work_entity_tag, selectors in field_selectors.items():
        working_entity = file_obj.get_working_entity(work_entity_tag)
        if not validate_fields(working_entity, selectors):
            return 0
        
    return 1

def validate_fields(working_entity, selectors):
    valid = 1
    for field_name, selector in selectors.items():
        retrieved = working_entity.find(selector.get('xpath')).text
        # print("field {}: [{}] with [{}]".format(field_name, retrieved, \
        # selector.get('value')))
        if retrieved != selector.get('value'):
            valid = 0
            break
    return valid


def validate_attributes(working_entity, filters):
    valid = 1
    for attribute_name, attribute_dic in filters.items():
        retrieved = get_attribute(working_entity, attribute_name, attribute_dic)
        # print("attri {}: [{}] with [{}]".format(attribute_name, retrieved,\
        # attribute_dic.get('value')))
        if not validate_attribute(retrieved, attribute_dic.get('value')):
            valid = 0
            break
    return valid

def get_attribute (working_entity, attribute_name, attribute_dic):
    retrieved = None
    default_ = None
    if attribute_dic.get('default'):
        default_  = attribute_dic.get('default')

    retrieved = working_entity.get(attribute_name, default_)
    return retrieved

def validate_attribute(retrieved, expected):
    valid = 0

    if isinstance(expected, list):
        if retrieved in expected:
            valid = 1
    elif isinstance(expected, str):
        if retrieved == expected:
            valid = 1
    return valid


def get_args():
    parser = argparse.ArgumentParser(description='read the list of xml or trxml\
    files, generate a list of documents which is a random subset selected using\
    the specified requirements')

    parser.add_argument('--config', help='config file to config the selectors', type=str)
    parser.add_argument('--input_dir', help='dir contains all xml or trxml to filter',\
                        type=str)
    parser.add_argument('--output_file', help='type of the file to filter, xml or trxml',\
                        type=str, default='select_filelist.txt')
    parser.add_argument('--files_to_ignore', help='a list of filenames to ignore',\
                        type=str, default=None)

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
    max_per_account = int(config['nr_docs'] * config['max_per_account'])
    output_fh = open(args.output_file,'w')
    for file_path in files:
        file_size = os.path.getsize(file_path)
        if file_size < config['min_size']:
            continue
        file_obj = get_file_obj(config['input_type'], file_path)
        is_valid_file = validate_file(file_obj, config)
        if is_valid_file:
            account = file_obj.get_customer_account()

            if account is None:
                output_fh.write(file_path + "\n")
            else:
                if not accounts.get(account):
                    accounts[account] = 0
                if accounts[account] < max_per_account:
                    output_fh.write(file_path + "\n")
                else:
                    pass
                accounts[account] = accounts[account] + 1

    output_fh.close()


if __name__ == '__main__':
    args = get_args()
    main(args)
