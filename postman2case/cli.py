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

    parser.add_argument('output_testset_file', nargs='?',
        help="Optional. Specify converted YAML/JSON testset file.")

    args = parser.parse_args()

    if args.version:
        print("{}".format(__version__))
        exit(0)

    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=log_level)

    postman_testset_file = args.postman_testset_file
    output_testset_file = args.output_testset_file

    if not postman_testset_file or not postman_testset_file.endswith(".json"):
        logging.error("postman_testset_file file not specified.")
        sys.exit(1)

    output_file_type = "JSON"
    if not output_testset_file:
        postman_file = os.path.splitext(postman_testset_file)[0]
        output_testset_file = "{}.{}.{}".format(postman_file, "output", output_file_type.lower())
    else:
        output_file_suffix = os.path.splitext(output_testset_file)[1]
        if output_file_suffix in [".json"]:
            output_file_type = "JSON"
        else:
            logging.error("Converted file could only be in JSON format.")
            sys.exit(1)

    postman_parser = PostmanParser(postman_testset_file)
    postman_parser.gen_json(output_testset_file)

    return 0







