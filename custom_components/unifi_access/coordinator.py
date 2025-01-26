"""Coordinator for integration."""

from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant

from .unifi_access_lib.door import UnifiAccessDoorClient

_LOGGER = logging.getLogger(__name__)

class PollingCoordinator(DataUpdateCoordinator):
    """Polling coordinator."""

    def __init__(
            self,
            hass: HomeAssistant,
            ip: str,
            token: str,
    ):
        """Initialize coordinator."""

        super().__init__(
            hass,
            _LOGGER,
            name="Unifi Access polling coordinator",
            update_interval=timedelta(seconds=3),
        )

        self.door_client = UnifiAccessDoorClient(ip, token)

    async def _async_update_data(self):
        """Fetch data from API endpoint."""

        doors = await self.hass.async_add_executor_job(self.door_client.get_doors)
        
        return {
            "doors": doors
        }
