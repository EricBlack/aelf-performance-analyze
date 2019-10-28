#! /usr/bin/python3
# -*- coding: utf-8 -*-


import requests
import json

import rout


class ApiService(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_request(self, api, *args):
        sub_url = rout.ApiCollection.sub_url(api)
        url = self.base_url + str(sub_url).format(args)\
            .replace("'", "").replace(",", "").replace("(", "").replace(")", "")
        response = requests.get(url)

        return response

    @staticmethod
    def print_result(info):
        formatted_json = json.dumps(json.loads(info), indent=2)
        print(formatted_json)
