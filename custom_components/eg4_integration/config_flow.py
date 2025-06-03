"""Adds config flow for EG4 Integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from slugify import slugify

from .api import (
    EG4ApiClient,
    EG4ApiClientAuthenticationError,
    EG4ApiClientCommunicationError,
    EG4ApiClientError,
)
from .const import DOMAIN, LOGGER


class EG4FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for EG4 Integration."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                )
            except EG4ApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except EG4ApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except EG4ApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    ## Do NOT use this in production code
                    ## The unique_id should never be something that can change
                    ## https://developers.home-assistant.io/docs/config_entries_config_flow_handler#unique-ids
                    unique_id=slugify(user_input[CONF_USERNAME])
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=(user_input or {}).get(CONF_USERNAME, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(CONF_PASSWORD): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, username: str, password: str) -> None:
        """Validate credentials."""
        client = EG4ApiClient(
            username=username,
            password=password,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Validate user input here
            return self.async_create_entry(title="EG4 Integration", data=user_input)

        data_schema = vol.Schema({
            vol.Required("inverter_model"): selector({"select": {"options": [
                "flexboss21", "flexboss18", "18kpv", "12kpv", "12000xp", "6000xp", "3000ehv", "gridboss"
            ]}}),
            vol.Required("battery_model"): selector({"select": {"options": [
                "wallmount indoor 100ah", "wallmount all weather", "wallmount indoor 280ah", "LL-S 48V 100ah", "LL 24V 200ah", "LL 12V 400ah", "lifepower4 48V v2", "lifepower4 24V v2"
            ]}}),
            vol.Required("inverter_serial_number"): selector({"text": {"multiline": False}}),
            vol.Optional("gridboss_serial_number"): selector({"text": {"multiline": False}}),
            vol.Required("polling_interval", default=10): vol.All(
                vol.Coerce(int),
                vol.Range(min=5) if self.connection_type == "TCP" else vol.Range(min=1)
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "description": "Configure your EG4 Integration. For help, visit: https://github.com/n2aws/hacs-eg4-integration"
            }
        )
