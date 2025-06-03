import pytest
from homeassistant import config_entries
from custom_components.eg4_integration.config_flow import EG4FlowHandler

@pytest.mark.asyncio
async def test_config_flow(hass):
    flow = EG4FlowHandler()
    result = await flow.async_step_user(user_input={
        "inverter_model": "Model A",
        "inverter_serial_number": "12345",
        "gridboss_serial_number": "67890",
        "polling_interval": 30,
    })

    assert result["type"] == "create_entry"
    assert result["title"] == "EG4 Integration"
    assert result["data"]["inverter_model"] == "Model A"
    assert result["data"]["polling_interval"] == 30
