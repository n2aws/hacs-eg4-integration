import pytest
from pymodbus.exceptions import ModbusException
from custom_components.eg4_integration.api import EG4ApiClient

@pytest.mark.asyncio
async def test_tcp_connection():
    client = EG4ApiClient(host="127.0.0.1", port=502)
    await client.connect()
    assert client.client.connected
    await client.close()
    assert client.client is None

@pytest.mark.asyncio
async def test_serial_connection():
    client = EG4ApiClient(serial_port="/dev/ttyUSB0", baudrate=9600)
    await client.connect()
    assert client.client.connected
    await client.close()
    assert client.client is None

@pytest.mark.asyncio
async def test_read_data():
    client = EG4ApiClient(host="127.0.0.1", port=502)
    await client.connect()
    with pytest.raises(ModbusException):
        await client.read_data(100, 1)
    await client.close()

@pytest.mark.asyncio
async def test_invalid_connection():
    client = EG4ApiClient()
    with pytest.raises(ValueError):
        await client.connect()

@pytest.mark.asyncio
async def test_auto_discover_ip():
    client = EG4ApiClient(serial_number="123456789")
    discovered_ip = await client.auto_discover_ip()
    assert discovered_ip == "192.168.1.89", "IP discovery failed for serial number 123456789"

@pytest.mark.asyncio
async def test_auto_discover_ip_no_serial():
    client = EG4ApiClient()
    with pytest.raises(ValueError):
        await client.auto_discover_ip()
