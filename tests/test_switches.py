import pytest
from homeassistant.components.switch import SwitchEntity
from custom_components.eg4_integration.switch import ENTITY_DESCRIPTIONS, EG4Switch

@pytest.mark.asyncio
async def test_switch_entities(hass):
    coordinator = hass.data["eg4_integration"]
    switches = [EG4Switch(coordinator, description) for description in ENTITY_DESCRIPTIONS]

    for switch in switches:
        assert isinstance(switch, SwitchEntity)
        assert switch.is_on is not None

@pytest.mark.asyncio
async def test_switch_toggle(hass):
    coordinator = hass.data["eg4_integration"]
    coordinator.data = {
        "notifications_enabled": False,
        "alerts_enabled": True,
    }

    switches = [EG4Switch(coordinator, description) for description in ENTITY_DESCRIPTIONS]

    for switch in switches:
        await switch.async_turn_on()
        assert coordinator.data[switch.entity_description.key] is True

        await switch.async_turn_off()
        assert coordinator.data[switch.entity_description.key] is False
