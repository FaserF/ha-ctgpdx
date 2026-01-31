"""DataUpdateCoordinator for the CTGP Deluxe Version integration."""
from __future__ import annotations

import re


from aiohttp import ClientError
from bs4 import BeautifulSoup

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DOMAIN,
    LOGGER,
    URL,
    UPDATE_INTERVAL,
    ATTR_VERSION,
    ATTR_DOWNLOAD_SIZE,
    ATTR_UNPACKED_SIZE,
    ATTR_RELEASE_DATE,
)


class CtgpdxUpdateCoordinator(DataUpdateCoordinator[dict[str, str]]):
    """Class to manage fetching CTGP-DX data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, str]:
        """Fetch data from the CTGP-DX website."""
        try:
            session = async_get_clientsession(self.hass)
            async with session.get(URL, timeout=10) as response:
                response.raise_for_status()
                html = await response.text()
        except ClientError as err:
            raise UpdateFailed(
                f"Error communicating with CTGP-DX server: {err}"
            ) from err
        except Exception as err:
            raise UpdateFailed(
                f"Unexpected error fetching data: {err}"
            ) from err

        try:
            soup = BeautifulSoup(html, "html.parser")
            data = {}

            # 1. Extract Version
            # Looking for "Version: 1.1.1" or similar in text nodes
            version_match = re.search(r"Version:\s*([\d\.]+)", soup.get_text())
            if version_match:
                data[ATTR_VERSION] = version_match.group(1)
            else:
                # Fallback: look for "CTGP Deluxe (1.1.1)"
                version_match = re.search(
                    r"CTGP Deluxe \(([\d\.]+)\)", soup.get_text()
                )
                if version_match:
                    data[ATTR_VERSION] = version_match.group(1)

            # 2. Extract Sizes
            size_match = re.search(
                r"Download size:\s*([\d\.]+\s*[GM]B)", soup.get_text(), re.I
            )
            if size_match:
                data[ATTR_DOWNLOAD_SIZE] = size_match.group(1)

            unpacked_match = re.search(
                r"Unpacked size:\s*([\d\.]+\s*[GM]B)", soup.get_text(), re.I
            )
            if unpacked_match:
                data[ATTR_UNPACKED_SIZE] = unpacked_match.group(1)

            # 3. Extract Release Date
            # Looking for changelog header like "v1.1.1 - March 23rd, 2025"
            if ATTR_VERSION in data:
                ver_escaped = data[ATTR_VERSION].replace(".", r"\.")
                date_pattern = (
                    fr"v{ver_escaped}\s*-\s*([A-Za-z]+\s+\d+\w*,\s+\d{{4}})"
                )
                date_match = re.search(date_pattern, soup.get_text())
                if date_match:
                    data[ATTR_RELEASE_DATE] = date_match.group(1)

            if not data:
                raise UpdateFailed(
                    "Could not find any data on the CTGP-DX page."
                )

            if ATTR_VERSION not in data:
                LOGGER.warning(
                    "Version not found in page content, but found other data."
                )

            LOGGER.debug("Successfully fetched CTGP-DX data: %s", data)
            return data

        except Exception as err:
            LOGGER.error("Error parsing CTGP-DX website: %s", err)
            raise UpdateFailed(f"Error parsing website: {err}") from err
