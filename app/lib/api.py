import urllib.parse

import requests


class BaseAPI:
    api_url = ""
    api_path = "/"
    params = {}

    def __init__(self, api_url):
        self.api_url = api_url

    def add_parameter(self, key, value):
        self.params[key] = value

    def build_query_string(self) -> str:
        return (
            "?" + urllib.parse.urlencode(self.params)
            if len(self.params)
            else ""
        )

    def get_results(self, page=None):
        if page:
            self.add_parameter("page", page)
        url = f"{self.api_url}{self.api_path}{self.build_query_string()}"
        # print(url)
        response = requests.get(url)
        if response.status_code == 404:
            raise Exception("Resource not found")
        if response.status_code == requests.codes.ok:
            return self.parse_response(response)
        raise ConnectionError("Request to API failed")

    def parse_response(self, response):
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            raise ConnectionError("API provided non-JSON response")
