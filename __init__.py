import logging
from homeassistant.core import HomeAssistant
#from homeassistant.helpers.discovery import async_load_platform

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    _LOGGER.debug("Setting up Yoda BLE via async_setup (YAML mode)")

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    return True
