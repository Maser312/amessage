"""
Anisette and Authentication HTTP Headers Formatter
"""

import time
import base64
import hashlib
from typing import Dict
from .generator import AppleHardwareProfile

class AnisetteHeaders:
    @staticmethod
    def build_headers(profile: AppleHardwareProfile, local_user_id: str = "0") -> Dict[str, str]:
        client_timestamp = int(time.time())

        seed = f"{profile.serial_number}:{profile.mlb}:{client_timestamp}".encode("utf-8")
        otp_hash = hashlib.sha256(seed).digest()
        x_apple_md = base64.b64encode(otp_hash[:16]).decode("utf-8")

        m_seed = f"{profile.platform_uuid}:{profile.board_id}".encode("utf-8")
        x_apple_md_m = base64.b64encode(hashlib.sha256(m_seed).digest()[:16]).decode("utf-8")

        x_apple_md_rinfo = "17106176"

        return {
            "X-Apple-I-MD": x_apple_md,
            "X-Apple-I-MD-M": x_apple_md_m,
            "X-Apple-I-MD-RINFO": x_apple_md_rinfo,
            "X-Apple-I-MD-LU": local_user_id,
            "X-Apple-I-SRL-NO": profile.serial_number,
            "X-Apple-I-Client-Time": str(client_timestamp),
            "User-Agent": f"iMessage/13.0 ({profile.model}; macOS 13.6.4)"
        }
