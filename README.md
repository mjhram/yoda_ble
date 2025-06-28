# yoda_ble
A custom Home Assistant integration to passively monitor the Yoda1/okok Bluetooth scale via BLE advertisements.

### What integration does
parses weight from a okok/Yoda1 BLE scale

## Raspberry Pi Homeassistant requirements:
  - HACS should already be installed in HA
  - Add ESPHome (docker in case of docker HA)

## Installation instructions:
  - Manual copy the files in this repo __(/custom_components/yoda_ble/)__ to __&lt;HA config folder>/custom_components/yoda_ble/__ 
  - add the integration as a sensor to HA configuration.yaml as follows (address is the scale MAC address):
### configuration.yaml example
```
sensor:
  - platform: yoda_ble
    address: "D8:E7:2F:C8:BE:D3"
```
### What data is shown: weight and last_updated (as sensor attribute)

### Notes: 
- MAC address can be obtained from any tool, such as:
```
hcidump --raw
bluetoothctl
```
- Bluetooth Proxy was used because raspberry pi internal bluetooth didn't catch okok scal bluetooth messages (May because they have non-standard Company ID/MAC) 

## ESPHome:
  Install "Bluetooth proxy" from [Ready-Made projects](https://esphome.io/projects/)

## Credits
This integration was built with significant help from __ChatGPT__, especially for Bluetooth parsing, entity registration, and Home Assistant API usage.
