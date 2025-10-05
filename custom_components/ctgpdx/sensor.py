"""Sensor platform for the CTGP Deluxe Version integration."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_ICON, SENSOR_NAME


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    # Get the coordinator from the hass.data store
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Create the sensor entity and add it to Home Assistant
    async_add_entities([CtgpdxVersionSensor(coordinator, entry)])


class CtgpdxVersionSensor(CoordinatorEntity, SensorEntity):
    """Representation of a CTGP-DX Version sensor."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry_id = entry.entry_id

        # Set basic sensor attributes
        self._attr_name = SENSOR_NAME
        self._attr_icon = SENSOR_ICON

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the sensor."""
        return f"{self._entry_id}_ctgpdx_version"

    @property
    def state(self) -> str | None:
        """Return the state of the sensor."""
        # The state is the data fetched by the coordinator
        return self.coordinator.data

    @property
    def device_info(self):
        """Return device information for this sensor."""
        return {
            "identifiers": {(DOMAIN, "ctgpdx_version_sensor")},
            "name": "CTGP Deluxe",
            "manufacturer": "CTGP Deluxe Team",
            "model": "Version Tracker",
            "configuration_url": "https://www.ctgpdx.com/",
        }