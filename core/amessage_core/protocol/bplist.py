"""
Binary Property List (bplist) Serialization Helper
"""

import plistlib
from typing import Any

def serialize_bplist(data: Any) -> bytes:
    return plistlib.dumps(data, fmt=plistlib.FMT_BINARY)

def deserialize_bplist(data: bytes) -> Any:
    return plistlib.loads(data)
