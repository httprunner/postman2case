import argparse
import logging
import os
import sys

from postman2case import __version__
from postman2case.core import PostmanParser


def main():
    parser = argparse.ArgumentParser(
        description="Convert postman testcases to JSON testcases for HttpRunner.")
    parser.add_argument("-V", "--version", dest='version', action='store_true',
        help="show version")
    parser.add_argument('--log-level', default='INFO',
        help="Specify logging level, default is INFO.")

    parser.add_argument('postman_testset_file', nargs='?',
        help="Specify postman testset file.")

    parser.add_argument('--output_file_type', nargs='?',
        help="Optional. Specify output file type.")

    parser.add_argument('--output_dir', nargs='?',
        help="Optional. Specify output directory.")

    args = parser.parse_args()

    if args.version:
        print("{}".format(__version__))
        exit(0)

    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=log_level)

    postman_testset_file = args.postman_testset_file
    output_file_type = args.output_file_type
    output_dir = args.output_dir

    if not postman_testset_file or not postman_testset_file.endswith(".json"):
        logging.error("postman_testset_file file not specified.")
        sys.exit(1)
    
    if not output_file_type:
        output_file_type = "json"
    else:
        output_file_type = output_file_type.lower()
    if output_file_type not in ["json", "yml", "yaml"]:
        logging.error("output file only support json/yml/yaml.")
        sys.exit(1)
    
    if not output_dir:
        output_dir = '.'

    postman_parser = PostmanParser(postman_testset_file)
    parse_result = postman_parser.parse_data()
    postman_parser.save(parse_result, output_dir, output_file_type=output_file_type)

    return 0







