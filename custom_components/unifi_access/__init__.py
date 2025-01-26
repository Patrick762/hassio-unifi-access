"""Integration init"""

import logging
from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import PollingCoordinator
from .const import CONF_CONSOLE_IP, CONF_TOKEN, DATA_COORDINATOR, DOMAIN

PLATFORMS: List[Platform] = [Platform.BINARY_SENSOR]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""

    _LOGGER.debug("Init config entry for integration %s", DOMAIN)

    # Get config entries
    ip = entry.data.get(CONF_CONSOLE_IP)
    token = entry.data.get(CONF_TOKEN)

    # Create data structure
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(entry.entry_id, {})

    # Setup coordinator
    coordinator = PollingCoordinator(hass, ip, token)
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id].setdefault(DATA_COORDINATOR, coordinator)

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.debug("Setup done")

    return True
