"""
Anisette and Validation Data Client
Connects to headless amessage-relay, live public Anisette v3 server, or falls back to local spoofing.
"""

import logging
import base64
import requests
from typing import Dict, Optional, Tuple

from .generator import generate_hardware_profile, AppleHardwareProfile
from .headers import AnisetteHeaders

logger = logging.getLogger("amessage.anisette")

DEFAULT_PUBLIC_ANISETTE = "https://ani.sidestore.io"

class AnisetteClient:
    def __init__(self, relay_url: Optional[str] = None, relay_token: Optional[str] = None):
        self.relay_url = relay_url or DEFAULT_PUBLIC_ANISETTE
        self.relay_token = relay_token
        self.profile: AppleHardwareProfile = generate_hardware_profile()

    def get_anisette_headers(self) -> Dict[str, str]:
        if self.relay_url:
            try:
                headers = {}
                if self.relay_token:
                    headers["Authorization"] = f"Bearer {self.relay_token}"
                url = self.relay_url
                if "sidestore.io" in self.relay_url or self.relay_url.endswith("/"):
                    pass
                elif not self.relay_url.endswith("/headers"):
                    url = f"{self.relay_url}/api/v1/anisette/headers"
                resp = requests.get(url, headers=headers, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    logger.info("Successfully fetched genuine Anisette FairPlay headers.")
                    return data
            except Exception as e:
                logger.warning(f"Failed to fetch headers from relay ({e}), falling back to local generator.")

        return AnisetteHeaders.build_headers(self.profile)

    def get_validation_data(self) -> bytes:
        if self.relay_url and not "sidestore.io" in self.relay_url:
            try:
                headers = {"Content-Length": "0"}
                if self.relay_token:
                    headers["Authorization"] = f"Bearer {self.relay_token}"
                resp = requests.post(
                    f"{self.relay_url}/api/v1/bridge/get-validation-data",
                    headers=headers,
                    timeout=10
                )
                if resp.status_code == 200:
                    data_json = resp.json()
                    b64_val = data_json.get("data", "")
                    if b64_val:
                        return base64.b64decode(b64_val)
            except Exception as e:
                logger.warning(f"Relay validation call failed ({e}), using synthesized validation token.")

        payload = bytearray()
        payload.extend(b"\x01\x00\x00\x00")
        payload.extend(self.profile.rom)
        payload.extend(self.profile.serial_number.encode("utf-8"))
        return bytes(payload)
