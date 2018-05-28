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

    def read_postman_data(self):
        with open(self.postman_testcase_file) as file:
            postman_data = json.load(file)


        return postman_data
        
        

    def parse_each_item(self, item):
        temp = {}
        temp["name"] = item["name"]
        print(item)
        request = {}
        request["method"] = item["request"]["method"]
        if request["method"] == "POST":

            if "raw" in item["request"]["url"].keys():
                request["url"] = item["request"]["url"]["raw"]
            headers = {}
            for header in item["request"]["header"]:
                headers[header["key"]] = header["value"]
            request["headers"] = headers

            body = {}
            if item["request"]["body"] != {}:
                mode = item["request"]["body"]["mode"]
                for param in item["request"]["body"][mode]:
                    body[param["key"]] = param["value"]
            
            request["json "] = body
        else:
            if "raw" in item["request"]["url"].keys():
                url = item["request"]["url"]["raw"]
            request["url"] = url.split("?")[0]
            headers = {}
            for header in item["request"]["header"]:
                headers[header["key"]] = header["value"]
            request["headers"] = headers

            body = {}
            if "query" in item["request"]["url"].keys():
                for query in item["request"]["url"]["query"]:
                    body[query["key"]] = query["value"]
            
            request["params "] = body
        temp["request"] = request
        return temp



    def gen_json(self, output_testset_file):
        postman_data = self.read_postman_data()
        # print(postman_data)

        result = []

        for folder in postman_data["item"]:
            print(folder["name"])
            if "item" in folder["item"]:
                for item in folder["item"]:
                    temp = self.parse_each_item(item)
                    result.append(temp)
            else:
                temp = self.parse_each_item(folder)
                result.append(temp)

        print(result)


