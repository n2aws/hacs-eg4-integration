import pytest
from homeassistant.core import HomeAssistant

@pytest.mark.asyncio
async def test_dashboard_import(hass: HomeAssistant):
    dashboard_path = "config/dashboard.yaml"
    with open(dashboard_path, "r") as file:
        dashboard_content = file.read()

    assert "Battery Status" in dashboard_content
    assert "Charge Level" in dashboard_content
    assert "Inverter Performance" in dashboard_content
    assert "Alerts and Notifications" in dashboard_content
