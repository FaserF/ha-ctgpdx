"""DataUpdateCoordinator for the CTGP Deluxe Version integration."""

from __future__ import annotations

import re
from datetime import datetime, timezone, timedelta

from aiohttp import ClientError
from bs4 import BeautifulSoup

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.issue_registry import (
    async_create_issue,
    async_delete_issue,
    IssueSeverity,
)
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
        self._last_success_time: datetime | None = datetime.now(timezone.utc)

    async def _async_update_data(self) -> dict[str, str]:
        """Fetch data from the CTGP-DX website."""
        try:
            session = async_get_clientsession(self.hass)
            async with session.get(URL, timeout=10) as response:
                response.raise_for_status()
                html = await response.text()
        except ClientError as err:
            await self._async_handle_failure()
            raise UpdateFailed(
                f"Error communicating with CTGP-DX server: {err}"
            ) from err
        except Exception as err:
            await self._async_handle_failure()
            raise UpdateFailed(f"Unexpected error fetching data: {err}") from err

        try:
            soup = BeautifulSoup(html, "html.parser")
            data = {}

            # Normalize text: strip HTML and collapse whitespace
            raw_text = soup.get_text(separator=" ", strip=True)
            normalized_text = " ".join(raw_text.split())

            # 1. Extract Version
            # Match Version: followed by digits, dots, and internal spaces,
            # stopping before next keyword or uppercase word like "Download" or "Unpacked"
            version_pattern = (
                r"(?i:Version:)\s*([\d\.a-z\s]+?)(?=\s+(?:[A-Z]|Download|Unpacked)|$)"
            )
            version_match = re.search(version_pattern, normalized_text)
            if not version_match:
                # Priority 2: "CTGP Deluxe (1.1.1)"
                version_match = re.search(
                    r"(?i:CTGP Deluxe \()([\d\.a-z\s]+?)\)", normalized_text
                )

            if not version_match:
                # Priority 3: any string that looks like a version after "v"
                version_match = re.search(r"\bv([\d\.a-z\s]+?)\b", normalized_text, re.I)

            if version_match:
                # Clean up extracted version by removing internal spaces
                data[ATTR_VERSION] = version_match.group(1).replace(" ", "").strip()
            else:
                LOGGER.warning("Could not find version number in page content")

            # 2. Extract Sizes
            # Keywords "Download size" and "Unpacked size" can have internal spaces or typos
            # like "Download size :", "Unpacked s ize:", etc.
            size_pattern = r"Download.*?s\s*ize\s*:\s*([\d\.]+\s*[KMGT]?B)"
            size_match = re.search(size_pattern, normalized_text, re.I)
            if size_match:
                data[ATTR_DOWNLOAD_SIZE] = size_match.group(1)

            unpacked_pattern = r"Unpacked.*?s\s*ize\s*:\s*([\d\.]+\s*[KMGT]?B)"
            unpacked_match = re.search(unpacked_pattern, normalized_text, re.I)
            if unpacked_match:
                data[ATTR_UNPACKED_SIZE] = unpacked_match.group(1)

            # 3. Extract Release Date
            if ATTR_VERSION in data:
                ver_escaped = re.escape(data[ATTR_VERSION])
                date_pattern = rf"v?{ver_escaped}\s*-\s*([A-Za-z]+\s+\d+\w*,\s+\d{{4}})"
                date_match = re.search(date_pattern, normalized_text, re.I)
                if date_match:
                    data[ATTR_RELEASE_DATE] = date_match.group(1)

            if ATTR_RELEASE_DATE not in data:
                generic_date_match = re.search(
                    r"([A-Z][a-z]+\s+\d{1,2}(?:st|nd|rd|th)?,\s+20\d{2})",
                    normalized_text,
                )
                if generic_date_match:
                    data[ATTR_RELEASE_DATE] = generic_date_match.group(1)

            if not data:
                await self._async_handle_failure()
                raise UpdateFailed(
                    "Could not find any relevant data on the CTGP-DX page."
                )

            # Success!
            self._last_success_time = datetime.now(timezone.utc)
            async_delete_issue(self.hass, DOMAIN, "website_change")

            if ATTR_VERSION not in data:
                LOGGER.warning("Version not found, but extracted other data: %s", data)

            LOGGER.debug("Successfully fetched CTGP-DX data: %s", data)
            return data

        except UpdateFailed:
            raise
        except Exception as err:
            await self._async_handle_failure()
            LOGGER.error("Error parsing CTGP-DX website: %s", err)
            raise UpdateFailed(f"Error parsing website: {err}") from err

    async def _async_handle_failure(self) -> None:
        """Handle a failed update."""
        if self._last_success_time is None:
            # Should not happen as we initialize it, but just in case
            return

        if datetime.now(timezone.utc) - self._last_success_time > timedelta(hours=24):
            async_create_issue(
                self.hass,
                DOMAIN,
                "website_change",
                is_fixable=False,
                severity=IssueSeverity.WARNING,
                translation_domain=DOMAIN,
                translation_key="website_change",
                learn_more_url="https://github.com/FaserF/ha-ctgpdx/issues",
            )
