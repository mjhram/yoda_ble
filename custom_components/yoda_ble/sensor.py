import binascii
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfMass
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components.bluetooth import (
    async_register_callback,
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
)

from .const import DOMAIN
from .weight_sensor import YodaScaleWeightSensor
from .ble_parser import parse_yoda_manufacturer_data
from .weight_sensor import YodaScaleWeightSensor

_LOGGER = logging.getLogger(__name__)

CONF_ADDR = "address"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.debug("Setting up Yoda BLE sensors from async_setup_platform")
    
    snsr = YodaScaleWeightSensor(config[CONF_ADDR])
    
    def _handle_ble_advertisement(service_info: BluetoothServiceInfoBleak, change) -> None:
        #_LOGGER.debug("Received BLE advertisement from %s", service_info.address)
        _LOGGER.debug("BLE from %s (%s)", service_info.address, service_info.name)
        _LOGGER.debug("Manufacturer data: %s", service_info.manufacturer_data)

        #if service_info.local_name != "Yoda1": #gives error 'habluetooth.models.BluetoothServiceInfoBleak' object has no attribute 'local_name'
        #    return
        # Look through all manufacturer data keys
        for key, value in service_info.manufacturer_data.items():
            if key & 0xFF == 0xC0:  # 2nd byte is 0xC0 (lower byte in LE)
                _LOGGER.info("🎯 Matched Yoda1-like manufacturer ID: 0x%04X", key)
                _LOGGER.info("value[6]: 0x%02X", value[6])
                _LOGGER.info("value: %s", value)
                #_LOGGER.info(f"raw bytes: {value!r}")
                _LOGGER.info("raw bytes: %s", binascii.hexlify(value).decode('ascii')) 
                if value[6] == 0x25:
                    _LOGGER.info("hass.async_create_task")
                    hass.async_create_task(process_advertisement(hass, service_info))
                    break
                
    async def process_advertisement(hass, service_info):
        #_LOGGER.debug("Received BLE advertisement: %s", service_info)
        #_LOGGER.debug("Received BLE advertisement from %s", service_info.address)
        #_LOGGER.debug("Full advertisement: %s", service_info)
        # Entity update code goes here
        if service_info.name != "Yoda1":
            _LOGGER.debug("Ignored advertisement from %s", service_info.name)
            return

        parsed = parse_yoda_manufacturer_data(service_info.manufacturer_data)
        if not parsed:
            _LOGGER.debug("Failed to parse manufacturer data: %s", service_info.manufacturer_data)
            return

        address = service_info.address
        weight = parsed["weight"]
        _LOGGER.info("Parsed weight %.2f kg from %s", weight, address)

        #for entry in hass.config_entries.async_entries(DOMAIN):
        if address == snsr._address:
            snsr.update_weight(weight)
            _LOGGER.info("Entry address: %s", snsr._address)
            return
        else:
            _LOGGER.info("Entry address: %s is not matching with msg address: %s", snsr._address, address)
                
        #if address not in entities:
        #    _LOGGER.info("Sensor not exist for %s", address)
            #sensor = YodaScaleWeightSensor(address)
            #entities[address] = sensor
            ##hass.helpers.entity_platform.async_get_current_platform().async_add_entities([sensor])
            #hass.async_create_task(
            #    hass.helpers.entity_component.async_add_entities(hass, [sensor], "sensor")
            #)
            #entities[address].update_weight(weight)
        #else:
        #    _LOGGER.debug("Updating existing sensor for %s", address)
        #    entities[address].update_weight(weight)

    if snsr:
        async_add_entities([snsr])
        _LOGGER.debug("async_setup_platform: Entity Added %s", snsr )
    
    async_register_callback(
        hass,
        _handle_ble_advertisement,
        {},
        BluetoothScanningMode.PASSIVE,
    )

    _LOGGER.debug("Bluetooth callback registered")

