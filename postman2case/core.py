import io
import json
import logging
import os
import yaml
from collections import OrderedDict

from postman2case.compat import ensure_ascii
from postman2case.parser import parse_value_from_type


class PostmanParser(object):
    def __init__(self, postman_testcase_file):
        self.postman_testcase_file = postman_testcase_file

    def read_postman_data(self):
        with open(self.postman_testcase_file, encoding='utf-8', mode='r') as file:
            postman_data = json.load(file)

        return postman_data
    
    def parse_url(self, request_url):
        url = ""
        if isinstance(request_url, str):
            url = request_url
        elif isinstance(request_url, dict):
            if "raw" in request_url.keys():
                url= request_url["raw"]
        return url
    
    def parse_header(self, request_header):
        headers = {}
        for header in request_header:
            headers[header["key"]] = header["value"]
        return headers

    def parse_each_item(self, item):
        """ parse each item in postman to testcase in httprunner
        """
        api = {}
        api["name"] = item["name"]
        api["validate"] = []
        api["variables"] = []

        request = {}
        request["method"] = item["request"]["method"]

        url = self.parse_url(item["request"]["url"])

        if request["method"] == "GET":
            request["url"] = url.split("?")[0]
            request["headers"] = self.parse_header(item["request"]["header"])

            body = {}
            if "query" in item["request"]["url"].keys():
                for query in item["request"]["url"]["query"]:
                    api["variables"].append({query["key"]: parse_value_from_type(query["value"])})
                    body[query["key"]] = "$"+query["key"]
            request["params"] = body
        else:
            request["url"] = url
            request["headers"] = self.parse_header(item["request"]["header"])

            body = {}
            if item["request"]["body"] != {}:
                mode = item["request"]["body"]["mode"]
                if isinstance(item["request"]["body"][mode], list):
                    for param in item["request"]["body"][mode]:
                        if param["type"] == "text":
                            api["variables"].append({param["key"]: parse_value_from_type(param["value"])})
                        else:
                            api["variables"].append({param["key"]: parse_value_from_type(param["src"])})
                        body[param["key"]] = "$"+param["key"]
                elif isinstance(item["request"]["body"][mode], str):
                    
                    body = item["request"]["body"][mode]
            request["data"] = body

        api["request"] = request
        return api
    
    def parse_items(self, items, folder_name=None):
        result = []
        for folder in items:
            if "item" in folder.keys():
                name = folder["name"].replace(" ", "_")
                if folder_name:
                    name = os.path.join(folder_name, name)
                temp = self.parse_items(folder["item"], name)
                result += temp
            else:
                api = self.parse_each_item(folder)
                api["folder_name"] = folder_name
                result.append(api)
        return result

    def parse_data(self):
        """ dump postman data to json testset
        """
        logging.info("Start to generate JSON testset.")
        postman_data = self.read_postman_data()

        result = self.parse_items(postman_data["item"], None)
        return result

    def save(self, data, output_dir, output_file_type="json"):
        count = 0
        output_dir = os.path.join(output_dir, "api")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for each_api in data:
            count += 1
            file_name = str(count) + "." + output_file_type
            
            folder_name = each_api.pop("folder_name")
            if folder_name:
                folder_path = os.path.join(output_dir, folder_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = os.path.join(folder_path, file_name)
            else:
                file_path = os.path.join(output_dir, file_name)
            if os.path.isfile(file_path):
                logging.error("{} file had exist.".format(file_path))
                continue
            if output_file_type == "json":
                with io.open(file_path, 'w', encoding="utf-8") as outfile:
                    my_json_str = json.dumps(each_api, ensure_ascii=ensure_ascii, indent=4)
                    if isinstance(my_json_str, bytes):
                        my_json_str = my_json_str.decode("utf-8")

                    outfile.write(my_json_str)
            else:
                with io.open(file_path, 'w', encoding="utf-8") as outfile:
                    my_json_str = json.dumps(each_api, ensure_ascii=ensure_ascii, indent=4)
                    yaml.dump(each_api, outfile, allow_unicode=True, default_flow_style=False, indent=4)
                    
            logging.info("Generate JSON testset successfully: {}".format(file_path))
            