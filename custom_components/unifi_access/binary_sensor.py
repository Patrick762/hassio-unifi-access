"""Binary sensors."""

import logging

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass

from .unifi_access_lib.door import DOOR_BINARY, Door, UnifiAccessDoorClient

from .const import CONF_CONSOLE_IP, CONF_TOKEN, DATA_COORDINATOR, DOMAIN
from .coordinator import PollingCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Setup binary_sensor entities."""

    # Get config entries
    ip = entry.data.get(CONF_CONSOLE_IP)
    token = entry.data.get(CONF_TOKEN)

    door_client = UnifiAccessDoorClient(ip, token)
    doors = await hass.async_add_executor_job(door_client.get_doors)

    door_sensors = []
    for door in doors:
        for key in DOOR_BINARY:
            if door.__dict__[key] == "":
                _LOGGER.debug("Skipping " + door.full_name + " - " + key)
                continue

            device_class = None
            state_on = None

            match key:
                case "door_lock_relay_status":
                    device_class = BinarySensorDeviceClass.LOCK
                    state_on = "unlock"
                case "door_position_status":
                    device_class = BinarySensorDeviceClass.DOOR
                    state_on = "open"

            if device_class is None or state_on is None:
                continue

            door_sensors.append(
                DoorBinarySensor(
                    hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR],
                    door.full_name,
                    door.id,
                    key,
                    device_class,
                    state_on
                )
            )

    async_add_entities(door_sensors)

class DoorBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary door sensor."""

    def __init__(
        self,
        coordinator: PollingCoordinator,
        name: str,
        id: str,
        key: str,
        device_class: BinarySensorDeviceClass,
        state_on: str,
    ):
        """Init entity."""
        super().__init__(coordinator)

        self.coordinator = coordinator
        self.id = id # Door id
        self.name = name # Door name
        self.key = key # Key (which value of the door, relay or position f.ex.)
        self.state_on = state_on

        self._attr_has_entity_name = True
        self._attr_name = name + " - " + key # TODO: translate key
        self._attr_unique_id = id + key
        self._attr_device_class = device_class

        self._attr_available = False

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        data = self.coordinator.data

        if data is None:
            _LOGGER.warning(
                "Data from coordinator is None",
            )
            self.set_state(False)
            return

        if not isinstance(data, dict):
            _LOGGER.warning(
                "Invalid data from coordinator (not dict)",
            )
            self.set_state(False)
            return

        doors = data.get("doors")

        if not isinstance(doors, list):
            _LOGGER.warning(
                "Invalid data from coordinator (not list)",
            )
            self.set_state(False)
            return
        
        for door in doors:
            if not isinstance(door, Door):
                _LOGGER.warning(
                    "Invalid data from coordinator (not Door)",
                )
                continue

            if door.id == self.id:
                state = door.__dict__[self.key]

                if state is None or state == "":
                    _LOGGER.warning(
                        "Invalid data from coordinator (state %s - %s not readable)",
                        self.id,
                        self.key,
                    )
                    self.set_state(False)
                    return

                self.set_state(True, state == self.state_on)

    def set_state(self, available: bool, state: bool | None):
        """Easy way to set states and update."""

        self._attr_available = available

        if state is not None:
            self._attr_is_on = state

        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._attr_available
