import logging
_LOGGER = logging.getLogger(__name__)

def parse_yoda_manufacturer_data(manufacturer_data: dict):
    for key, data in manufacturer_data.items():
        if key & 0xFF == 0xC0 and len(data) >= 4:
            # Extract weight from bytes 2-3
            weight_raw = int.from_bytes(data[0:2], "big")
            weight_kg = weight_raw / 100
            return {"weight": weight_kg}
    return None


