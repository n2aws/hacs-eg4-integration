"""Custom types for EG4 Integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import EG4ApiClient
    from .coordinator import EG4DataUpdateCoordinator


type EG4ConfigEntry = ConfigEntry[EG4Data]


@dataclass
class EG4Data:
    """Data for the EG4 integration."""

    client: EG4ApiClient
    coordinator: EG4DataUpdateCoordinator
    integration: Integration
