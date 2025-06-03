import pytest
from homeassistant.components.sensor import SensorEntity
from custom_components.eg4_integration.sensor import ENTITY_DESCRIPTIONS, EG4Sensor

@pytest.mark.asyncio
async def test_sensor_entities(hass):
    coordinator = hass.data["eg4_integration"]
    sensors = [EG4Sensor(coordinator, description) for description in ENTITY_DESCRIPTIONS]

    for sensor in sensors:
        assert isinstance(sensor, SensorEntity)
        assert sensor.native_value is not None
        assert sensor.entity_description.key in coordinator.data

@pytest.mark.asyncio
async def test_sensor_data(hass):
    coordinator = hass.data["eg4_integration"]
    coordinator.data = {
        "battery_status": 80,
        "charge_level": 50,
        "inverter_performance": 95,
    }

    sensors = [EG4Sensor(coordinator, description) for description in ENTITY_DESCRIPTIONS]

    for sensor in sensors:
        assert sensor.native_value == coordinator.data[sensor.entity_description.key]
