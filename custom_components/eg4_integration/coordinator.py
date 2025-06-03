"""DataUpdateCoordinator for EG4 Integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from datetime import timedelta

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    EG4ApiClientAuthenticationError,
    EG4ApiClientError,
    EG4ApiClient,
)

if TYPE_CHECKING:
    from .data import EG4ConfigEntry


MODBUS_MAP = {
    "battery_status": 100,
    "charge_level": 101,
    "inverter_performance": 102,
    "alert_status": 200,
}

MODBUS_MAP_GRIDBOSS = {
    "gridboss_status": 300,
    "gridboss_alert": 301,
}


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class EG4IntegrationDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: EG4ConfigEntry

    def __init__(self, hass, api_client, config_entry):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name="EG4 Integration",
            update_interval=timedelta(seconds=30),
        )
        self.api_client = api_client
        self.config_entry = config_entry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.api_client.get_data()
        except EG4ApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except EG4ApiClientError as error:
            raise UpdateFailed(f"Error fetching data: {error}") from error


class EG4DataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the EG4 hardware."""

    def __init__(self, hass, config_entry):
        super().__init__(
            hass,
            LOGGER,
            name="EG4 Integration",
            update_interval=timedelta(seconds=config_entry.data.get("polling_interval", 30)),
        )
        self.api_client = EG4ApiClient(
            host=config_entry.data.get("host"),
            port=config_entry.data.get("port"),
            serial_port=config_entry.data.get("serial_port"),
            baudrate=config_entry.data.get("baudrate", 9600),
        )

    async def _async_update_data(self):
        """Fetch data from the Modbus registers."""
        try:
            await self.api_client.connect()
            data = {
                key: await self.api_client.read_data(address, 1)[0]
                for key, address in MODBUS_MAP.items()
            }

            # Fetch GridBoss data if configured
            if self.config_entry.data.get("gridboss_serial_number"):
                gridboss_data = {
                    key: await self.api_client.read_data(address, 1)[0]
                    for key, address in MODBUS_MAP_GRIDBOSS.items()
                }
                data.update(gridboss_data)

            await self.api_client.close()
            return data
        except Exception as error:
            raise UpdateFailed(f"Error fetching data: {error}")
