#! /usr/bin/python3

import requests
import json

from requests import Response

import rout


class ApiService(object):
    request_header = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, base_url):
        self.base_url = base_url

    def get_request(self, api, *args):
        sub_url = rout.ApiCollection.sub_url(api)
        url = self.base_url + str(sub_url).format(args) \
            .replace("'", "").replace(",", "").replace("(", "").replace(")", "")
        response = requests.get(url, headers=self.request_header)
        if response.status_code != 200:
            raise Exception(response.reason)

        return response

    def post_request(self, api, json_params):
        sub_url = rout.ApiCollection.sub_url(api)
        url = self.base_url + str(sub_url)
        response = requests.post(url, json=json_params, headers=self.request_header)
        if response.status_code != 200:
            raise Exception(response.reason)

        return response


def print_result(info):
    formatted_json = json.dumps(json.loads(info), indent=2)
    print(formatted_json)
