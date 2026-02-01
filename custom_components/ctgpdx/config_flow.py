"""Config flow for the CTGP Deluxe Version integration."""

from __future__ import annotations

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    # In this case, we don't discover devices, so we just check
    # if an entry already exists. This prevents multiple instances.
    return len(hass.config_entries.async_entries(DOMAIN)) > 0


class CtgpdxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CTGP Deluxe Version."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # Check if an entry is already configured
        if await _async_has_devices(self.hass):
            return self.async_abort(reason="single_instance_allowed")

        # If the user submits the form (even an empty one)
        if user_input is not None:
            # We don't have any data to store from the user, so data is empty.
            return self.async_create_entry(title="CTGP Deluxe", data={})

        # Show the user a form with no fields, just a submit button.
        return self.async_show_form(step_id="user")
