"""
Apple Bag URL Configuration Resolver
Fetches active dynamic endpoints for Madrid, IDS, and APNs services
"""

import plistlib
import logging
import requests

logger = logging.getLogger("amessage.bags")

DEFAULT_BAG_URL = "https://init-p01st.push.apple.com/bag"

FALLBACK_BAG = {
    "init-validation": "https://service.ess.apple.com/WebObjects/TDSService.woa/wa/initializeValidation",
    "register": "https://service.ess.apple.com/WebObjects/TDSService.woa/wa/register",
    "authenticate": "https://identity.ess.apple.com/WebObjects/TDSService.woa/wa/authenticate",
    "lookup": "https://service.ess.apple.com/WebObjects/TDSService.woa/wa/search",
    "sign-in": "https://setup.icloud.com/setup/signin/v2/login",
    "gsa-auth": "https://gsa.apple.com/grandslam/GsService2"
}

class BagResolver:
    def __init__(self, bag_url: str = DEFAULT_BAG_URL):
        self.bag_url = bag_url
        self.bag_cache = FALLBACK_BAG.copy()

    def fetch_bag(self) -> dict:
        headers = {
            "User-Agent": "iMessage/13.0 (MacBookPro16,1; macOS 13.6.4)"
        }
        try:
            resp = requests.get(self.bag_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = plistlib.loads(resp.content)
                self.bag_cache.update(data)
                logger.debug("Successfully updated Apple service bag URLs.")
        except Exception as e:
            logger.warning(f"Failed to fetch live Apple bag URL, using cached fallbacks: {e}")
        return self.bag_cache

    def get_url(self, key: str) -> str:
        return self.bag_cache.get(key, FALLBACK_BAG.get(key, ""))
