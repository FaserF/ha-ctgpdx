"""Sensor platform for the CTGP Deluxe Version integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    ATTR_VERSION,
    ATTR_DOWNLOAD_SIZE,
    ATTR_UNPACKED_SIZE,
    ATTR_RELEASE_DATE,
)
from .coordinator import CtgpdxUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: CtgpdxUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        CtgpdxSensor(
            coordinator,
            entry,
            ATTR_VERSION,
            "Latest Version",
            "mdi:nintendo-switch",
        ),
        CtgpdxSensor(
            coordinator,
            entry,
            ATTR_DOWNLOAD_SIZE,
            "Download Size",
            "mdi:download-network",
            enabled_default=False,
        ),
        CtgpdxSensor(
            coordinator,
            entry,
            ATTR_UNPACKED_SIZE,
            "Unpacked Size",
            "mdi:folder-zip",
            enabled_default=False,
        ),
    ]

    async_add_entities(entities)


class CtgpdxSensor(CoordinatorEntity[CtgpdxUpdateCoordinator], SensorEntity):
    """Representation of a CTGP-DX sensor."""

    def __init__(
        self,
        coordinator: CtgpdxUpdateCoordinator,
        entry: ConfigEntry,
        sensor_type: str,
        name_suffix: str,
        icon: str,
        enabled_default: bool = True,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry_id = entry.entry_id
        self._sensor_type = sensor_type
        self._attr_name = f"CTGP-DX {name_suffix}"
        self._attr_icon = icon
        self._attr_unique_id = f"{entry.entry_id}_ctgpdx_{sensor_type}"
        self._attr_entity_registry_enabled_default = enabled_default

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(self._sensor_type)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, str] | None:
        """Return the extra state attributes."""
        if (
            self._sensor_type == ATTR_VERSION
            and self.coordinator.data
            and (release_date := self.coordinator.data.get(ATTR_RELEASE_DATE))
        ):
            return {ATTR_RELEASE_DATE: release_date}
        return None

    @property
    def device_info(self):
        """Return device information for this sensor."""
        return {
            "identifiers": {(DOMAIN, "ctgpdx_version_sensor")},
            "name": "CTGP Deluxe",
            "manufacturer": "CTGP Deluxe Team",
            "model": "Version Tracker",
            "configuration_url": "https://www.ctgpdx.com/download",
        }
