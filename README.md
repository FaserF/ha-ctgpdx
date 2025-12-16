[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

# CTGP Deluxe Home Assistant Sensor 🏎️

The `ctgpdx` sensor provides the latest [CTGP Deluxe](https://www.ctgpdx.com/) version available, allowing you to get notified when updates are released.

## Features ✨

- **Latest Version**: Tracks the current version of CTGP Deluxe.
- **Update Notifications**: Use automations to get alerted on new releases.

## Installation 🛠️

### 1. Using HACS (Recommended)

This integration can be added to HACS as a **Custom Repository**.

1.  Open HACS.
2.  Click on the 3 dots in the top right corner -> **Custom repositories**.
3.  Add `https://github.com/FaserF/ha-ctgpdx` and select category **Integration**.
4.  Click **Download**.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=FaserF&repository=ha-ctgpdx&category=integration)

### 2. Manual Installation

1.  Download the latest [Release](https://github.com/FaserF/ha-ctgpdx/releases/latest).
2.  Extract the ZIP file.
3.  Copy the `ctgpdx` folder to `<config>/custom_components/`.

## Configuration ⚙️

1.  Go to **Settings** -> **Devices & Services**.
2.  Click **Add Integration**.
3.  Search for "CTGP Deluxe Version".

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ctgpdx)

### Configuration Variables
None needed.

## Automations
```yaml
- id: 'ctgpdx_new_version_notification'
  alias: 'CTGP-DX: New Version Available'
  description: 'Notifies when the CTGP Deluxe version sensor changes to a valid state.'
  trigger:
    - platform: state
      entity_id: sensor.ctgp_dx_latest_version
  condition:
    - condition: template
      value_template: "{{ trigger.to_state.state not in ['unknown', 'unavailable'] }}"
    - condition: template
      value_template: "{{ trigger.from_state.state not in ['unknown', 'unavailable'] }}"
    - condition: template
      value_template: "{{ trigger.to_state.state != trigger.from_state.state }}"
  action:
    - service: notify.mobile_app_your_device
      data:
        title: '🎉 New CTGP-DX Version Available!'
        message: >
          New version **{{ trigger.to_state.state }}** is now available!
          (Previous version: {{ trigger.from_state.state }})
        data:
          url: "[https://www.ctgpdx.com/download](https://www.ctgpdx.com/download)"
  mode: single
```

## Bug reporting
Open an issue over at [github issues](https://github.com/FaserF/ha-ctgpdx/issues). Please prefer sending over a log with debugging enabled.

To enable debugging enter the following in your configuration.yaml

```yaml
logger:
    logs:
        custom_components.ctgpdx: debug
```

You can then find the log in the HA settings -> System -> Logs -> Enter "ctgpdx" in the search bar -> "Load full logs"

## Thanks to
The data is coming from the corresponding [ctgpdx.com](https://www.ctgpdx.com/download) website.
