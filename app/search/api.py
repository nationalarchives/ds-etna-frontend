import json

import requests
from app.lib import BaseAPI
from flask import current_app


class BaseSearchAPI(BaseAPI):
    def __init__(self):
        super().__init__(current_app.config.get("SEARCH_API_URL"))

    def query(self, value):
        self.add_parameter("q", value)


class RecordsAPI(BaseSearchAPI):
    api_path = "/records/"


class ArticlesAPI(BaseSearchAPI):
    api_path = "/articles/"

    def parse_response(self, response):
        try:
            if current_app.config.get("ENVIRONMENT") == "develop":
                text = response.text
                text = text.replace(
                    "https://main-bvxea6i-ncoml7u56y47e.uk-1.platformsh.site/",
                    "http://localhost:65535/",
                ).replace(
                    "https://develop-sr3snxi-rasrzs7pi6sd4.uk-1.platformsh.site/",
                    "http://localhost:65535/",
                )
                return json.loads(text)
            return response.json()
        except requests.exceptions.JSONDecodeError:
            current_app.logger.error("API provided non-JSON response")
            raise ConnectionError("API provided non-JSON response")
