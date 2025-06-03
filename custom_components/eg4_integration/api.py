"""Sample API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout
from pymodbus.client.async_tcp import AsyncModbusTcpClient
from pymodbus.client.async_serial import AsyncModbusSerialClient


class EG4ApiClientError(Exception):
    """Exception to indicate a general API error."""


class EG4ApiClientCommunicationError(EG4ApiClientError):
    """Exception to indicate a communication error."""


class EG4ApiClientAuthenticationError(EG4ApiClientError):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise EG4ApiClientAuthenticationError(msg)
    response.raise_for_status()


class EG4ApiClient:
    """API Client for EG4 Integration."""

    def __init__(
        self,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url="https://jsonplaceholder.typicode.com/posts/1",
        )

    async def async_set_title(self, value: str) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise EG4ApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise EG4ApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise EG4ApiClientError(
                msg,
            ) from exception


class EG4ApiClient:
    """API client for EG4 hardware."""

    def __init__(
        self,
        host: str = None,
        port: int = None,
        serial_port: str = None,
        baudrate: int = 9600,
        serial_number: str = None,
    ):
        self.host = host
        self.port = port
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.serial_number = serial_number
        self.client = None

    async def auto_discover_ip(self):
        """Auto-discover the IP address using mDNS."""
        if self.serial_number:
            try:
                # Use mDNS to discover devices on the network
                mdns_query = f"EG4-{self.serial_number}.local"
                discovered_ip = socket.gethostbyname(mdns_query)
                self.host = discovered_ip
                return discovered_ip
            except socket.error as e:
                raise ConnectionError(f"Failed to auto-discover IP: {e}")
        raise ValueError("Serial number is required for IP auto-discovery.")

    async def connect(self):
        """Establish connection to EG4 hardware."""
        if self.serial_port:
            # Serial connection logic
            self.client = AsyncModbusSerialClient(
                method="rtu", port=self.serial_port, baudrate=self.baudrate
            )
        elif self.host:
            # TCP/IP connection logic
            self.client = AsyncModbusTcpClient(host=self.host, port=self.port)
        elif self.serial_number:
            # Attempt IP auto-discovery
            await self.auto_discover_ip()
            self.client = AsyncModbusTcpClient(host=self.host, port=self.port)
        else:
            raise ValueError("Either host or serial_port must be provided.")

        try:
            await self.client.connect()
        except ConnectionError:
            # Retry IP auto-discovery if connection fails
            if self.serial_number:
                await self.auto_discover_ip()
                self.client = AsyncModbusTcpClient(host=self.host, port=self.port)
                await self.client.connect()
            else:
                raise

    async def read_data(self, address: int, count: int):
        """Read data from EG4 hardware."""
        if not self.client:
            raise ConnectionError("Client is not connected.")

        response = await self.client.read_holding_registers(address, count)
        return response.registers

    async def close(self):
        """Close the connection."""
        if self.client:
            await self.client.close()
            self.client = None
