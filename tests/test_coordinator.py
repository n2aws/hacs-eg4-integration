import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed
from custom_components.eg4_integration.coordinator import EG4DataUpdateCoordinator

@pytest.mark.asyncio
async def test_update_data(hass):
    config_entry = {
        "data": {
            "host": "127.0.0.1",
            "port": 502,
            "polling_interval": 30,
        }
    }
    coordinator = EG4DataUpdateCoordinator(hass, config_entry)
    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()

@pytest.mark.asyncio
async def test_gridboss_data(hass):
    config_entry = {
        "data": {
            "host": "127.0.0.1",
            "port": 502,
            "gridboss_serial_number": "12345",
        }
    }
    coordinator = EG4DataUpdateCoordinator(hass, config_entry)
    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()
