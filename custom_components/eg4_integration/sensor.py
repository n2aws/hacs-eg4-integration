"""Sensor platform for EG4 Integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import EG4Entity

if TYPE_CHECKING:
    from .coordinator import EG4DataUpdateCoordinator
    from .data import EG4ConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="battery_status",
        name="Battery Status",
        icon="mdi:battery",
    ),
    SensorEntityDescription(
        key="charge_level",
        name="Charge Level",
        icon="mdi:battery-charging",
    ),
    SensorEntityDescription(
        key="inverter_performance",
        name="Inverter Performance",
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="gridboss_status",
        name="GridBoss Status",
        icon="mdi:server",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: EG4ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: EG4DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        EG4Sensor(
            coordinator=entry.runtime_data.coordinator,
            description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class EG4Sensor(EG4Entity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(
        self,
        coordinator: EG4DataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{description.key}"

    @property
    def native_value(self):
        """Return the native value from the coordinator data."""
        return self.coordinator.data.get(self.entity_description.key)
