# hassio-bluetti-bt

Bluetti BLE Integration for Home Assistant (fork of [Patrick762/hassio-bluetti-bt](https://github.com/Patrick762/hassio-bluetti-bt))

## What this fork adds

- **AP300 support** with correct Modbus slave address (0 for 2nd-gen IoT devices)
- **Encrypted write controls** for switches and selects on encrypted devices (AP300, etc.)
- **Manual config flow** allowing device setup by BLE MAC address
- **Vendored library loading** so the integration works without `pip install` from git URLs
- **Structured BLE error handling** with `DeviceNotFoundError`, `ConnectionFailedError`, `EncryptionHandshakeError`

Uses the [cinderblock/bluetti-bt-lib](https://github.com/cinderblock/bluetti-bt-lib) fork of the underlying library.

## Installation

### HACS (Custom Repository)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. In HACS, go to Integrations > three-dot menu > Custom repositories
3. Add `https://github.com/cinderblock/hassio-bluetti-bt` as an Integration
4. Install "Bluetti BT" from HACS
5. **Important:** You must also vendor the library manually (HACS doesn't handle git-based pip deps):
   ```bash
   # From a machine with SSH access to your HA host:
   git clone https://github.com/cinderblock/bluetti-bt-lib /tmp/bluetti-bt-lib
   ssh root@YOUR_HA_HOST 'mkdir -p /config/deps'
   scp -r /tmp/bluetti-bt-lib/bluetti_bt_lib root@YOUR_HA_HOST:/config/deps/
   ```
6. Restart Home Assistant

### Manual Installation

```bash
git clone https://github.com/cinderblock/hassio-bluetti-bt /tmp/hassio-bluetti-bt
git clone https://github.com/cinderblock/bluetti-bt-lib /tmp/bluetti-bt-lib

scp -r /tmp/hassio-bluetti-bt/custom_components/bluetti_bt root@YOUR_HA_HOST:/config/custom_components/
ssh root@YOUR_HA_HOST 'mkdir -p /config/deps'
scp -r /tmp/bluetti-bt-lib/bluetti_bt_lib root@YOUR_HA_HOST:/config/deps/
```

Restart Home Assistant after copying.

## Adding the device

The integration supports Bluetooth auto-discovery (BLE name patterns like `AP3*`, `AC2*`, etc.) and manual setup via the Integrations UI. If auto-discovery doesn't trigger, you can add the device manually by entering its BLE MAC address.

For AP300 and other encrypted 2nd-gen devices, the config entry can also be injected directly into `.storage/core.config_entries` — see [setup notes](https://github.com/cinderblock/hassio-bluetti-bt/wiki) for details.

## Supported devices

See [bluetti-bt-lib supported devices](https://github.com/cinderblock/bluetti-bt-lib#supported-powerstations-and-data)

## Example Dashboard (AP300)

To create a dedicated Bluetti dashboard, go to Settings > Dashboards > Add Dashboard, then switch to the raw configuration editor (three-dot menu > Edit dashboard > Raw configuration editor) and paste the YAML below.

Replace `YOUR_DEVICE_ID` with your device's entity prefix (e.g. `ap3002526010030108` — visible in Settings > Devices).

```yaml
views:
  - title: AP300
    path: ap300
    icon: mdi:battery-charging
    type: masonry
    cards:
      - type: gauge
        entity: sensor.YOUR_DEVICE_ID_battery_soc
        name: Battery
        unit: '%'
        min: 0
        max: 100
        severity:
          green: 50
          yellow: 20
          red: 0
        needle: true
      - type: entities
        title: Status
        entities:
          - entity: sensor.YOUR_DEVICE_ID_time_remaining
            name: Time Remaining
          - entity: sensor.YOUR_DEVICE_ID
            name: Working Mode
          - entity: sensor.YOUR_DEVICE_ID_charging_mode
            name: Charging Mode
      - type: glance
        title: Power
        columns: 3
        entities:
          - entity: sensor.YOUR_DEVICE_ID_ac_input_power
            name: AC In
          - entity: sensor.YOUR_DEVICE_ID_dc_input_power
            name: Solar In
          - entity: sensor.YOUR_DEVICE_ID_ac_output_power
            name: AC Out
      - type: entities
        title: Switches
        show_header_toggle: false
        entities:
          - entity: switch.YOUR_DEVICE_ID_ac_output
            name: AC Output
          - entity: switch.YOUR_DEVICE_ID_eco_mode_ac
            name: ECO Mode AC
          - entity: switch.YOUR_DEVICE_ID_power_lifting
            name: Power Lifting
      - type: entities
        title: Settings
        show_header_toggle: false
        entities:
          - entity: select.YOUR_DEVICE_ID
            name: Working Mode
          - entity: select.YOUR_DEVICE_ID_charging_mode
            name: Charging Mode
          - entity: select.YOUR_DEVICE_ID_display_timeout
            name: Display Timeout
      - type: entities
        title: AC Input
        entities:
          - entity: sensor.YOUR_DEVICE_ID_ac_input_voltage
            name: Voltage
          - entity: sensor.YOUR_DEVICE_ID_ac_input_current
            name: Current
          - entity: sensor.YOUR_DEVICE_ID_ac_input_frequency
            name: Frequency
      - type: entities
        title: AC Output
        entities:
          - entity: sensor.YOUR_DEVICE_ID_ac_output_voltage
            name: Voltage
          - entity: sensor.YOUR_DEVICE_ID_ac_output_frequency
            name: Frequency
      - type: entities
        title: Device Info
        entities:
          - entity: sensor.YOUR_DEVICE_ID_device_type
            name: Model
          - entity: sensor.YOUR_DEVICE_ID_serial_number
            name: Serial Number
```

## Disclaimer

This integration is provided without any warranty or support by Bluetti. Use at your own risk.
