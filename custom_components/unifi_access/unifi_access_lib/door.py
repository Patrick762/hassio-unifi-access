"""Unifi Access Door Client."""

from typing import List

from .api import UnifiAccessApiClient

EP_DOORS = "/api/v1/developer/doors"
DOOR_BINARY = ["door_lock_relay_status", "door_position_status"]

class Door:
    def __init__(
        self,
        door: dict,
    ):
        self.door_lock_relay_status = door["door_lock_relay_status"]
        self.door_position_status = door["door_position_status"]
        self.floor_id = door["floor_id"]
        self.full_name = door["full_name"]
        self.id = door["id"]
        self.is_bind_hub = door["is_bind_hub"]
        self.name = door["name"]
        self.type = door["type"]

class UnifiAccessDoorClient(UnifiAccessApiClient):
    def __init__(self, ip: str, token: str):
        super().__init__(ip, token)

    def get_door(self, id: str) -> Door:
        return super().get(EP_DOORS + "/" + id)

    def get_doors(self) -> List[Door]:
        doors = super().get(EP_DOORS).json()["data"]
        objects = []
        for door in doors:
            objects.append(Door(door))
        return objects
