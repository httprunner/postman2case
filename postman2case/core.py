import base64
import io
import json
import logging
import sys
from collections import OrderedDict

import yaml

class PostmanParser(object):
    def __init__(self, postman_testcase_file):
        self.postman_testcase_file = postman_testcase_file