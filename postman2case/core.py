import base64
import io
import json
import logging
import sys

from postman2case.compat import ensure_ascii

from collections import OrderedDict


class PostmanParser(object):
    def __init__(self, postman_testcase_file):
        self.postman_testcase_file = postman_testcase_file

    def read_postman_data(self):
        with open(self.postman_testcase_file, 'r') as file:
            postman_data = json.load(file)

        return postman_data
        

    def parse_each_item(self, item):
        """ parse each item in postman to testcase in httprunner
        """
        temp = {}
        temp["name"] = item["name"]
        temp["validate"] = []

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
            request["json"] = body
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
            request["params"] = body

        temp["request"] = request
        return temp



    def gen_json(self, output_testset_file):
        """ dump postman data to json testset
        """
        logging.debug("Start to generate JSON testset.")
        postman_data = self.read_postman_data()

        result = []

        for folder in postman_data["item"]:
            if "item" in folder.keys():
                for item in folder["item"]:
                    temp = self.parse_each_item(item)
                    result.append({"test":temp})
            else:
                temp = self.parse_each_item(folder)
                result.append(temp)

        with io.open(output_testset_file, 'w', encoding="utf-8") as outfile:
            my_json_str = json.dumps(result, ensure_ascii=ensure_ascii, indent=4)
            if isinstance(my_json_str, bytes):
                my_json_str = my_json_str.decode("utf-8")

            outfile.write(my_json_str)
        logging.info("Generate JSON testset successfully: {}".format(output_testset_file))


