from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import CtgpdxUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up CTGP-DX from a config entry."""
    # Ensure the visit button points to the download page
    hass.config_entries.async_update_entry(
        entry, configuration_url="https://www.ctgpdx.com/download"
    )

    coordinator = CtgpdxUpdateCoordinator(hass)

    # Fetch initial data so we have it when the sensor is set up

    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator object
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Set up the platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    ):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
