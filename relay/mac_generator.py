"""
Standalone SMBIOS and Serial Number Generator for AMessage Relay
"""

import uuid
import random
import string
from typing import Dict, Any

def generate_mac_profile() -> Dict[str, Any]:
    models = ["MacBookPro16,1", "iMac19,1", "Macmini8,1"]
    chosen_model = random.choice(models)

    location = "C02"
    year_code = random.choice(["K", "L", "M"])
    week_code = random.choice(string.ascii_uppercase)
    unique_seq = "".join(random.choices(string.ascii_uppercase + string.digits, k=3))
    model_code = "MD6T" if "MacBook" in chosen_model else "JV3G"
    serial = f"{location}{year_code}{week_code}{unique_seq}{model_code}"

    mlb_suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=14))
    mlb = f"{location}{mlb_suffix}"

    mac_prefix = [0xAC, 0xDE, 0x48]
    mac_suffix = [random.randint(0x00, 0xFF) for _ in range(3)]
    rom_bytes = bytes(mac_prefix + mac_suffix)

    return {
        "model": chosen_model,
        "serial_number": serial,
        "mlb": mlb,
        "rom": rom_bytes.hex(),
        "platform_uuid": str(uuid.uuid4()).upper(),
        "board_id": "Mac-E1008331FDC96864" if "MacBook" in chosen_model else "Mac-AA95B1DDAB278B95"
    }
