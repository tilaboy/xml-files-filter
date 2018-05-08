#!/usr/bin/env python

import sys
import argparse
from os import listdir
import os
from os.path import isfile, join


def get_args():
    parser = argparse.ArgumentParser(description='read the list of xml files, filter on size, max number of documents from one account, filter fixed format, and language, return a sample of data, and filter against a given list')
    parser.add_argument('--input_dir', help='dir contains all xml or trxml to filter')
    parser.add_argument('--input_type', help='type of the file to filter, xml or trxml')
    parser.add_argument('--lang', help='language to filter', type=str)
    parser.add_argument('--number', help='number of CVs', type=int)
    parser.add_argument('--size', help='minimal document size, in kb', type=int)
    parser.add_argument('--noFixedFormat', help='filter out all fixed format document', action='store_true')
    parser.add_argument('--onlyWordOrPDF', help='filter out all document except word and pdf', action='store_true')
    return parser.parse_args()

def main(args):
    xml_dir = args.xml_dir
    files = [join(xml_dir, f) for f in listdir(xml_dir) if isfile(join(xml_dir, f))]
    allowed_types = ("pdf", "msword")
    accounts = {}
    for file_path in files:
        # print("checking file {}".format(file_path))
        is_good_size = size_ok(file_path, args.size)
        if not is_good_size:
            continue

        with open(file_path) as f:
            begin_line = f.readline()
            begin_line = f.readline()
        # print(begin_line)
        is_good_lang = lang_match(begin_line, args.lang)
        is_good_type = type_match(begin_line, allowed_types)
        is_not_ff = format_match(begin_line)
        if is_good_lang and is_good_type and is_not_ff:
            account = get_account(begin_line)
            if account:
                if account in accounts:
                    accounts[account] = accounts[account] + 1
                else:
                    accounts[account] = 0
                if accounts[account] < 1000:
                    print (file_path)
            else:
                print(file_path)

if __name__ == '__main__':
    args = get_args()
    main(args)
