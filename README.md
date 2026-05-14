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

## Disclaimer

This integration is provided without any warranty or support by Bluetti. Use at your own risk.
