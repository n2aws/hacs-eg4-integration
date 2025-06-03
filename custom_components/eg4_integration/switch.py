"""Switch platform for EG4 Integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .entity import EG4Entity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EG4DataUpdateCoordinator
    from .data import EG4ConfigEntry

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="notifications_enabled",
        name="Notifications Enabled",
        icon="mdi:bell",
    ),
    SwitchEntityDescription(
        key="alerts_enabled",
        name="Alerts Enabled",
        icon="mdi:alert",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: EG4ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switches based on a config entry."""
    coordinator: EG4DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        EG4Switch(coordinator, description)
        for description in ENTITY_DESCRIPTIONS
    )


class EG4Switch(EG4Entity, SwitchEntity):
    """Representation of a Switch."""

    def __init__(
        self,
        coordinator: EG4DataUpdateCoordinator,
        description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.coordinator.data.get(self.entity_description.key)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.coordinator.api_client.write_register(MODBUS_MAP[self.entity_description.key], 1)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.coordinator.api_client.write_register(MODBUS_MAP[self.entity_description.key], 0)
        self.async_write_ha_state()
