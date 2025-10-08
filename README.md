[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
# CTGP Deluxe version Homeassistant Sensor
The `ctgpdx` sensor will give you a sensor with the latest version available.

## Installation
### 1. Using HACS (recommended way)

This integration is no official HACS Integration and right now an custom integration.

Open HACS then install the "ctgpdx" integration or use the link below.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=FaserF&repository=ha-ctgpdx&category=integration)

If you use this method, your component will always update to the latest version.

### 2. Manual

- Download the latest zip release from [here](https://github.com/FaserF/ha-ctgpdx/releases/latest)
- Extract the zip file
- Copy the folder "ctgpdx" from within custom_components with all of its components to `<config>/custom_components/`

where `<config>` is your Home Assistant configuration directory.

>__NOTE__: Do not download the file by using the link above directly, the status in the "master" branch can be in development and therefore is maybe not working.

## Configuration

Go to Configuration -> Integrations and click on "add integration". Then search for "CTGP Deluxe Version".

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
