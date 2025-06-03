"""Binary sensor platform for EG4 Integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import EG4Entity

if TYPE_CHECKING:
    from .coordinator import EG4DataUpdateCoordinator
    from .data import EG4ConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="alert_status",
        name="Alert Status",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    BinarySensorEntityDescription(
        key="gridboss_alert",
        name="GridBoss Alert",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: EG4ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    coordinator: EG4DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        EG4BinarySensor(coordinator, description)
        for description in ENTITY_DESCRIPTIONS
    )


class EG4BinarySensor(EG4Entity, BinarySensorEntity):
    """Representation of a Binary Sensor."""

    def __init__(
        self,
        coordinator: EG4DataUpdateCoordinator,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{description.key}"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self.coordinator.data.get(self.entity_description.key)
