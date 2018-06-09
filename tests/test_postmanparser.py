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
        with open("tests/data/test.json") as f:
            content = json.load(f)
        other_content = self.postman_parser.read_postman_data()
        self.assertEqual(content, other_content)
    
    def test_parse_each_item_get(self):
        item = {
			"name": "test_get",
			"request": {
				"url": {
					"raw": "http://www.baidu.com?search=345",
					"protocol": "http",
					"host": [
						"www",
						"baidu",
						"com"
					],
					"query": [
						{
							"key": "search",
							"value": "345",
							"equals": True,
							"description": ""
						}
					],
					"variable": []
				},
				"method": "GET",
				"header": [],
				"body": {},
				"description": ""
			},
			"response": []
		}
        result = {
            "name": "test_get",
            "def": "test_get",
            "validate": [],
            "request": {
                "method": "GET",
                "url": "http://www.baidu.com",
                "headers": {},
                "params": {
                    "search": "345"
                }
            }
        }

        fun_result = self.postman_parser.parse_each_item(item)
        self.assertEqual(result, fun_result)
    
    def test_parse_each_item_post(self):
        item = {
			"name": "test_post",
			"request": {
				"url": "http://www.baidu.com",
				"method": "POST",
				"header": [],
				"body": {
					"mode": "formdata",
					"formdata": [
						{
							"key": "search",
							"value": "123",
							"description": "",
							"type": "text"
						}
					]
				},
				"description": ""
			},
			"response": []
		}
        result = {
            "name": "test_post",
            "def": "test_post",
            "validate": [],
            "request": {
                "method": "POST",
                "url": "http://www.baidu.com",
                "headers": {},
                "json": {
                    "search": "123"
                }
            }
        }
        fun_result = self.postman_parser.parse_each_item(item)
        self.assertEqual(result, fun_result)
    
    def test_gen_json(self):
        output_file = "tests/data/output.json"
        self.postman_parser.gen_json(output_file)
        os.remove(output_file)
        
