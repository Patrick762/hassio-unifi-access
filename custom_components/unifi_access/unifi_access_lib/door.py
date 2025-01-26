"""Unifi Access Door Client."""

from .api import UnifiAccessApiClient

EP_DOORS = "/api/v1/developer/doors"

class UnifiAccessDoor(UnifiAccessApiClient):
    def __init__(self, ip: str, token: str):
        super().__init__(ip, token)

    def get_door(id: str):
        return super().get(EP_DOORS + "/" + id)

    def get_doors():
        return super().get(EP_DOORS)
