"""Integration config flow"""

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_CONSOLE_IP, CONF_TOKEN, DOMAIN

class AccessConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for integration."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle user input."""

        if user_input is not None:
            ip = user_input[CONF_CONSOLE_IP]
            await self.async_set_unique_id(ip, raise_on_progress=False)
            self._abort_if_unique_id_configured()

            # TODO Test connection

            return self.async_create_entry(
                title="Console " + ip,
                data={
                    CONF_CONSOLE_IP: user_input[CONF_CONSOLE_IP],
                    CONF_TOKEN: user_input[CONF_TOKEN]
                },
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_CONSOLE_IP): str,
                vol.Required(CONF_TOKEN): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )
