"""The CTGP Deluxe Version integration."""
import re
from aiohttp import ClientError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from bs4 import BeautifulSoup

from .const import DOMAIN, LOGGER, PLATFORMS, UPDATE_INTERVAL, URL


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up CTGP-DX from a config entry."""

    # Create a aiohttp session
    session = async_get_clientsession(hass)

    async def _async_update_data():
        """Fetch the latest version from the ctgpdx website."""
        try:
            # Perform the GET request to the URL
            async with session.get(URL) as response:
                response.raise_for_status()
                html = await response.text()

                # Parse the HTML with BeautifulSoup
                soup = BeautifulSoup(html, "html.parser")

                # Find all <p> tags and iterate through them
                all_p_tags = soup.find_all("p")
                for p_tag in all_p_tags:
                    # Check if the text "Version:" is inside the tag's text
                    if "Version:" in p_tag.get_text():
                        # Extract the full text from the tag
                        full_text = p_tag.get_text()

                        # Use regex to find the version number pattern
                        match = re.search(r"Version:\s*([\d\.]+)", full_text)

                        if match:
                            # If a match is found, return the version string
                            version = match.group(1)
                            LOGGER.debug(f"Successfully fetched CTGP-DX version: {version}")
                            return version

                # If loop finishes without finding the version, raise an error
                LOGGER.error("Could not find the version pattern in the HTML content.")
                raise UpdateFailed("Could not find version information on the page.")

        except ClientError as err:
            LOGGER.error(f"Error communicating with {URL}: {err}")
            raise UpdateFailed(f"Error communicating with server: {err}")

    # Create the DataUpdateCoordinator
    coordinator = DataUpdateCoordinator(
        hass,
        LOGGER,
        name=DOMAIN,
        update_method=_async_update_data,
        update_interval=UPDATE_INTERVAL,
    )

    # Fetch initial data so we have it when the sensor is set up
    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator object
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Set up the platforms (sensor in this case)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an integration is removed.
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok