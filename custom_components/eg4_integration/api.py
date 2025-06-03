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
    ):
        self.host = host
        self.port = port
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.client = None

    async def connect(self):
        """Establish connection to EG4 hardware."""
        if self.host and self.port:
            self.client = AsyncModbusTcpClient(self.host, self.port)
        elif self.serial_port:
            self.client = AsyncModbusSerialClient(
                method="rtu", port=self.serial_port, baudrate=self.baudrate
            )
        else:
            raise ValueError("Either TCP or serial connection parameters must be provided.")

        await self.client.connect()

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
