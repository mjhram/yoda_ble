import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfMass
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # available in Python 3.9+

_LOGGER = logging.getLogger(__name__)

class YodaScaleWeightSensor(SensorEntity):
    @property
    def extra_state_attributes(self):
        if self._last_updated:
            return {"last_updated": self._last_updated.isoformat()}
        return {}
        
    def __init__(self, address: str):
        self._last_updated = datetime.now(ZoneInfo("Asia/Baghdad"))  #datetime.min
        self._attr_unique_id = f"{address}_weight"
        self._attr_name = f"Yoda Weight"
        self._attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
        self._attr_device_class = "weight"
        self._attr_state_class = "measurement"
        self._address = address
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, address)},
            name="Yoda",
            manufacturer="Yoda",
            model="Yoda1 Scale",
        )
        self._weight = None
        self._initial_weight = None  # ← store early value if needed
        self._min_update_interval = timedelta(seconds=15)
        
    @property
    def native_value(self):
        return self._weight

    def update_weight(self, weight):
        nowt = datetime.now(ZoneInfo("Asia/Baghdad"))
        _LOGGER.debug("update_weight")
        if (nowt - self._last_updated) < self._min_update_interval: #and weight == self._weight:
            _LOGGER.debug("update_weight duplicate")
            _LOGGER.debug("duplicate. now: %s ,last: %s, diff=%s", nowt, self._last_updated, (nowt - self._last_updated))
            return
        self._last_updated = nowt
        if self.hass is None:
            self._initial_weight = weight  # ← store for later
            _LOGGER.debug("update later")
        else: 
            _LOGGER.debug("update_weight state")
            self._weight = weight
            self.async_write_ha_state()
        _LOGGER.debug("update_weight end")

    async def async_added_to_hass(self):
        """Called when entity is added to Home Assistant."""
        _LOGGER.debug("async_added_to_hass")
        if self._initial_weight is not None:
            self._weight = self._initial_weight
            self.async_write_ha_state()
