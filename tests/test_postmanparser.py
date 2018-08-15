import unittest
import os
import json
from postman2case.core import PostmanParser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.postman_parser = PostmanParser("tests/data/test.json")

    def test_init(self):
        self.assertEqual(self.postman_parser.postman_testcase_file, "tests/data/test.json")

    def test_read_postman_data(self):
        with open("tests/data/test.json", encoding='utf-8', mode='r') as f:
            content = json.load(f)
        other_content = self.postman_parser.read_postman_data()
        self.assertEqual(content, other_content)

    def test_parse_each_item_get(self):
        with open("tests/data/test_get.json", encoding='utf-8', mode='r') as f:
            item = json.load(f)
        
        result = {
            "name": "test_get",
            "def": "test_get",
            "validate": [],
            "variables": [
                {
                    "search": "345"
                }
            ],
            "request": {
                "method": "GET",
                "url": "http://www.baidu.com",
                "headers": {},
                "params": {
                    "search": "$search"
                }
            }
        }

        fun_result = self.postman_parser.parse_each_item(item)
        self.assertEqual(result, fun_result)

    def test_parse_each_item_post(self):
        with open("tests/data/test_post.json", encoding='utf-8', mode='r') as f:
            item = json.load(f)
        
        result = {
            "name": "test_post",
            "def": "test_post",
            "validate": [],
            "variables": [
                {
                    "search": "123"
                }
            ],
            "request": {
                "method": "POST",
                "url": "http://www.baidu.com",
                "headers": {},
                "json": {
                    "search": "$search"
                }
            }
        }
        fun_result = self.postman_parser.parse_each_item(item)
        self.assertEqual(result, fun_result)

    def test_gen_json(self):
        output_file = "tests/data/output.json"
        self.postman_parser.gen_json(output_file)
        os.remove(output_file)

