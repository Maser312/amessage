"""
MMCS (MobileMe Cloud Services) Attachments Handler
"""

import os
import hashlib
from typing import Tuple, Dict, Any
from ..ids.crypto import IDSCrypto

class AttachmentHandler:
    @staticmethod
    def encrypt_attachment(file_bytes: bytes, filename: str, mime_type: str) -> Tuple[bytes, Dict[str, Any]]:
        aes_key = os.urandom(16)
        iv = os.urandom(16)

        ciphertext = IDSCrypto.encrypt_payload_aes_ctr(file_bytes, aes_key, iv)
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        descriptor = {
            "name": filename,
            "mime_type": mime_type,
            "size": len(file_bytes),
            "key": aes_key.hex(),
            "iv": iv.hex(),
            "sha256": file_hash,
            "mmcs_url": f"https://content.icloud.com/attachments/{file_hash}"
        }

        return ciphertext, descriptor

    @staticmethod
    def decrypt_attachment(ciphertext: bytes, descriptor: Dict[str, Any]) -> bytes:
        aes_key = bytes.fromhex(descriptor["key"])
        iv = bytes.fromhex(descriptor["iv"])
        return IDSCrypto.decrypt_payload_aes_ctr(ciphertext, aes_key, iv)
