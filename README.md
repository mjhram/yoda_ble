# yoda_ble
Home Assistant integration for smart OKOK scale

# Installation:
## Raspberry Pi Homeassistant requirements:
  - HACS should already be installed in HA
  - Add ESPHome (docker in case of docker HA)
  - copy the files in this repo to <HA config folder>/custom_components/
  - add the integration as a sensor to HA configuration.yaml as follows (address is the scale MAC address):
```
sensor:
  - platform: yoda_ble
    address: "D8:E7:2F:C8:BE:D3"
```
### Notes: 
- MAC address can be obtained from any tool, such as:
```
hcidump --raw
bluetoothctl
```
- Bluetooth Proxy was used because raspberry pi internal bluetooth didn't catch okok scal bluetooth messages (May because they have non-standard Company ID/MAC) 

## ESPHome:
  Install "Bluetooth proxy" from [Ready-Made projects](https://esphome.io/projects/)
