
# CTGP Deluxe Home Assistant Sensor 🏎️

The `ctgpdx` sensor provides the latest [CTGP Deluxe](https://www.ctgpdx.com/) version available, allowing you to get notified when updates are released.

## Features ✨

- **Latest Version**: Tracks the current version of CTGP Deluxe.
- **Download Size**: Shows the size of the download package.
- **Unpacked Size**: Shows the required space on the SD card.
- **Release Date**: Displays when the latest version was released.
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
3.  Search for **CTGP Deluxe**.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ctgpdx)

### Configuration Variables
None needed.

## Sensors 📊

After installation, the suivant sensors will be available:

| Sensor | Name | Icon | Description |
|---|---|---|---|
| `sensor.ctgp_dx_latest_version` | CTGP-DX Latest Version | `mdi:nintendo-switch` | The current version number (includes Release Date as attribute) |
| `sensor.ctgp_dx_download_size` | CTGP-DX Download Size | `mdi:download-network` | Size of the ZIP file (Disabled by default) |
| `sensor.ctgp_dx_unpacked_size` | CTGP-DX Unpacked Size | `mdi:folder-zip` | Space needed on SD card (Disabled by default) |


## Automations 🤖

Below are several examples of how you can use this integration in your automations.

<details>
<summary><b>1. Basic Notification on New Version (Mobile App)</b></summary>

This automation sends a notification to your phone whenever a new version is detected.

```yaml
- id: 'ctgpdx_new_version_notification'
  alias: 'CTGP-DX: New Version Available'
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
          New version **{{ trigger.to_state.state }}** is now available (Released: {{ state_attr('sensor.ctgp_dx_latest_version', 'release_date') }}).
          Download size: {{ states('sensor.ctgp_dx_download_size') }}.
        data:
          url: "https://www.ctgpdx.com/download"
          clickAction: "https://www.ctgpdx.com/download"
  mode: single
```
</details>

<details>
<summary><b>2. Conditional Notification (Only if Update is Large)</b></summary>

Get notified only if the download size is greater than 2 GB.

```yaml
- alias: 'CTGP-DX: Large Update Alert'
  trigger:
    - platform: state
      entity_id: sensor.ctgp_dx_latest_version
  condition:
    - condition: template
      value_template: "{{ states('sensor.ctgp_dx_download_size') | replace(' GB', '') | float > 2.0 }}"
  action:
    - service: notify.persistent_notification
      data:
        title: 'Huge Update Detected'
        message: 'A large CTGP-DX update ({{ states("sensor.ctgp_dx_download_size") }}) is out! Make sure your SD card has space.'
```
</details>

<details>
<summary><b>3. Announcement via Smart Speaker (TTS)</b></summary>

Announce the update via Alexa or Google Home.

```yaml
- alias: 'CTGP-DX: Voice Announcement'
  trigger:
    - platform: state
      entity_id: sensor.ctgp_dx_latest_version
  condition:
    - condition: template
      value_template: "{{ trigger.to_state.state != trigger.from_state.state }}"
  action:
    - service: tts.google_say
      target:
        entity_id: media_player.living_room_speaker
      data:
        message: "Attention! A new version of CTGP Deluxe, version {{ states('sensor.ctgp_dx_latest_version') }}, has just been released."
```
</details>

<details>
<summary><b>4. Dashboard Alert (Conditional Card)</b></summary>

You can also use the version sensor to show a conditional card on your dashboard only when the version matches a certain pattern or changes.

```yaml
# In your Lovelace configuration
type: conditional
conditions:
  - entity: sensor.ctgp_dx_latest_version
    state_not: "unknown"
card:
  type: entities
  entities:
    - entity: sensor.ctgp_dx_latest_version
      name: "Latest Mod Version"
```
</details>

## Bug reporting
Open an issue over at [GitHub issues](https://github.com/FaserF/ha-ctgpdx/issues). Please prefer sending over a log with debugging enabled.

To enable debugging enter the following in your `configuration.yaml`:

```yaml
logger:
    logs:
        custom_components.ctgpdx: debug
```

## Thanks to
The data is scraped from the official [ctgpdx.com](https://www.ctgpdx.com/download) website. All credits for the mod go to the CTGP Deluxe Team!
