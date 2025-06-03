import pytest
from homeassistant.components.binary_sensor import BinarySensorEntity
from custom_components.eg4_integration.binary_sensor import ENTITY_DESCRIPTIONS, EG4BinarySensor

@pytest.mark.asyncio
async def test_binary_sensor_entities(hass):
    coordinator = hass.data["eg4_integration"]
    binary_sensors = [EG4BinarySensor(coordinator, description) for description in ENTITY_DESCRIPTIONS]

    for binary_sensor in binary_sensors:
        assert isinstance(binary_sensor, BinarySensorEntity)
        assert binary_sensor.is_on is not None

@pytest.mark.asyncio
async def test_binary_sensor_data(hass):
    coordinator = hass.data["eg4_integration"]
    coordinator.data = {
        "alert_status": True,
        "gridboss_alert": False,
    }

    binary_sensors = [EG4BinarySensor(coordinator, description) for description in ENTITY_DESCRIPTIONS]

    for binary_sensor in binary_sensors:
        assert binary_sensor.is_on == coordinator.data[binary_sensor.entity_description.key]
