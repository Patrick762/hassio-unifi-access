"""Unifi Access Base Client."""

import requests

from .const import PORT

class UnifiAccessApiClient:
    def __init__(self, ip: str, token: str):
        self.ip = ip
        self.token = token

        self.host = "https://" + ip + ":" + PORT
        self.headers = {"Authorization": "Bearer " + token}

    def endpoint(self, path: str):
        return self.host + path

    def get(self, path: str):
        return requests.get(self.endpoint(path), headers=self.headers)
