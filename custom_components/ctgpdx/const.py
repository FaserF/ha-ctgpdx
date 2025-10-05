"""Constants for the CTGP Deluxe Version integration."""
from datetime import timedelta
import logging

DOMAIN = "ctgpdx"
LOGGER = logging.getLogger(__package__)

# Configuration constants
PLATFORMS = ["sensor"]
CONF_NAME = "CTGP-DX Version"

# Update interval
UPDATE_INTERVAL = timedelta(days=1)

# Website to scrape
URL = "https://www.ctgpdx.com/download"

# Sensor details
SENSOR_NAME = "CTGP-DX Latest Version"
SENSOR_ICON = "mdi:nintendo-switch"