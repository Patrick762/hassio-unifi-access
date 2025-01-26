"""Integration init"""

import logging
from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS: List[Platform] = []
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""

    _LOGGER.debug("Init config entry for integration %s", DOMAIN)

    # Setup platforms
    #await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True
