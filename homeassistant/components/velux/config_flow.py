"""Config flow for velux integration."""
import logging

from pyvlx import PyVLX, PyVLXException
import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_HOST, CONF_PASSWORD

from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {vol.Required(CONF_HOST): str, vol.Required(CONF_PASSWORD): str}
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for youless."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                host = user_input[CONF_HOST]
                password = user_input[CONF_PASSWORD]

                pyvlx = PyVLX(host=host, password=password)
                await pyvlx.connect()

                await pyvlx.disconnect()

                return self.async_create_entry(
                    title=host,
                    data=user_input,
                )
            except PyVLXException:
                _LOGGER.exception("Cannot connect to KLF 200 gateway")
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
