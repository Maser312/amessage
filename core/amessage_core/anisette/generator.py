"""
SMBIOS and Hardware Identifier Generator
Synthesizes valid Apple hardware identifiers (Model, Serial, Board-ID, MLB, ROM)
using OpenCore/Clover algorithmic rules to bypass hardware requirements.
"""

import uuid
import random
import string
import hashlib

APPLE_MODELS = [
    {
        "model": "MacBookPro16,1",
        "board_id": "Mac-E1008331FDC96864",
        "year_codes": ["K", "L", "M", "N"],
        "model_code": "MD6T"
    },
    {
        "model": "iMac19,1",
        "board_id": "Mac-AA95B1DDAB278B95",
        "year_codes": ["J", "K", "L"],
        "model_code": "JV3G"
    },
    {
        "model": "Macmini8,1",
        "board_id": "Mac-7BA5B2D9E42DDD94",
        "year_codes": ["J", "K", "L"],
        "model_code": "KXPG"
    }
]

APPLE_OUI_PREFIXES = [
    [0x00, 0x17, 0xF2],
    [0x00, 0x1E, 0xC2],
    [0x00, 0x25, 0x00],
    [0x3C, 0x07, 0x54],
    [0xAC, 0xDE, 0x48],
    [0xF0, 0x18, 0x98]
]

class AppleHardwareProfile:
    def __init__(
        self,
        model: str,
        board_id: str,
        serial_number: str,
        mlb: str,
        rom: bytes,
        platform_uuid: str,
        root_disk_uuid: str
    ):
        self.model = model
        self.board_id = board_id
        self.serial_number = serial_number
        self.mlb = mlb
        self.rom = rom
        self.platform_uuid = platform_uuid
        self.root_disk_uuid = root_disk_uuid

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "board-id": self.board_id,
            "IOPlatformSerialNumber": self.serial_number,
            "MLB": self.mlb,
            "ROM": self.rom.hex(),
            "IOPlatformUUID": self.platform_uuid,
            "root_disk_uuid": self.root_disk_uuid,
            "IOMACAddress": self.rom.hex()
        }

def generate_hardware_profile(chosen_model: str = "MacBookPro16,1") -> AppleHardwareProfile:
    model_info = next((m for m in APPLE_MODELS if m["model"] == chosen_model), APPLE_MODELS[0])

    location = "C02"
    year_code = random.choice(model_info["year_codes"])
    week_chars = string.ascii_uppercase.replace("I", "").replace("O", "").replace("U", "")
    week_code = random.choice(week_chars)
    unique_seq = "".join(random.choices(string.ascii_uppercase + string.digits, k=3))
    model_code = model_info["model_code"]
    serial_number = f"{location}{year_code}{week_code}{unique_seq}{model_code}"

    mlb_suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=14))
    mlb = f"{location}{mlb_suffix}"

    prefix = random.choice(APPLE_OUI_PREFIXES)
    suffix = [random.randint(0x00, 0xFF) for _ in range(3)]
    rom_bytes = bytes(prefix + suffix)

    platform_uuid = str(uuid.uuid4()).upper()
    root_disk_uuid = str(uuid.uuid4()).upper()

    return AppleHardwareProfile(
        model=model_info["model"],
        board_id=model_info["board_id"],
        serial_number=serial_number,
        mlb=mlb,
        rom=rom_bytes,
        platform_uuid=platform_uuid,
        root_disk_uuid=root_disk_uuid
    )
