"""Constants for the CTGP Deluxe Version integration."""

from datetime import timedelta
import logging

from homeassistant.const import Platform

DOMAIN = "ctgpdx"
LOGGER = logging.getLogger(__package__)

# Configuration constants
PLATFORMS = [Platform.SENSOR]

# Update interval
UPDATE_INTERVAL = timedelta(hours=6)

# Website to scrape
URL = "https://www.ctgpdx.com/download"

# Sensor identifiers
ATTR_VERSION = "version"
ATTR_DOWNLOAD_SIZE = "download_size"
ATTR_UNPACKED_SIZE = "unpacked_size"
ATTR_RELEASE_DATE = "release_date"
