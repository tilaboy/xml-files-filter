#!/usr/bin/env python

import sys
import argparse
from os import listdir
import os
from os.path import isfile, join
from TKxml import TKxml
from TKtrxml import TKtrxml
from random import shuffle

def validate_file(file_obj, args):
    valid = 0
    allowed_types = ("pdf", "msword")
    if args.file_type == 'trxml':
        xml_file = os.path.join('/home/chao/workspace/data_2017/CVs/random_100k/xml/', file_obj.orig_filename + '.xml')
        try:
            xmlfile_obj = TKxml(xml_file)
        except Exception as e:
            print("ERROR: not able to create xml object from {}".format(xml_file))
            print(e)

    if xmlfile_obj.get_size() > args.size and xmlfile_obj.get_lang() == args.lang and xmlfile_obj.get_orig_filetype() in allowed_types and xmlfile_obj.get_pathtype() == args.pathtype:
        valid = 1
    else:

        print("NOT VALID:")
        print("\tsize: {}".format(xmlfile_obj.get_size()))
        print("\tlang: {}".format(xmlfile_obj.get_lang()))
        print("\ttype: {}".format(xmlfile_obj.get_orig_filetype()))
        print("\tpath: {}".format(xmlfile_obj.get_pathtype()))

    if args.country and valid == 1:
        country = file_obj.get_country()
        if country == args.country:
            print ("country matched")
        else:
            print ("country not matched: {} <> {}".format(country, args.country))
            valid = 0
    return valid



def get_args():
    parser = argparse.ArgumentParser(description='read the list of xml files, filter on size, max number of documents from one account, filter fixed format, and language, return a sample of data, and filter against a given list')
    parser.add_argument('--input_dir', help='dir contains all xml or trxml to filter')
    parser.add_argument('--input_type', help='type of the file to filter, xml or trxml')
    parser.add_argument('--lang', help='language to filter on', type=str)
    parser.add_argument('--country', help='country to filter on', type=str)
    parser.add_argument('--number', help='number of CVs', type=int)
    parser.add_argument('--size', help='minimal document size, in kb', type=int)
    parser.add_argument('--pathtype', help='filter out on path type', type=str, default='standard')
    return parser.parse_args()

def main(args):
    input_dir = args.input_dir
    files = []
    for f in listdir(input_dir):
        if isfile(join(input_dir, f)):
            files.append(join(input_dir, f))

    shuffle(files)

    #files = [join(input_dir, f) for f in listdir(input_dir) if isfile(join(input_dir, f))]
    accounts = {}
    max_per_account = int(args.number * 0.05)
    for file_path in files:
        print("checking file {}".format(file_path))
        if args.input_type == 'xml':
            try:
                file_obj = TKxml(file_path)
            except Exception as e:
                print("ERROR: not able to create xml object from {}".format(file_path))
                print(e)

        if args.input_type == 'trxml':
            try:
                file_obj = TKtrxml(file_path)
            except Exception as e:
                print("ERROR: not able to create trxml object from {}".format(file_path))
                print(e)

        valid_file = validate_file(file_obj, args)
        if valid_file:
            account = file_obj.get_account()
            if accounts[account] < max_per_account:
                print(file_path)
                accounts[account] = accounts[account] + 1

        print ( accounts )

if __name__ == '__main__':
    args = get_args()
    #TODO: country checking is not supported for xml
    main(args)
