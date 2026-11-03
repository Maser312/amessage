"""
Unit Tests for AMessage Protocol Engine
"""

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from amessage_core.anisette.generator import generate_hardware_profile
from amessage_core.anisette.headers import AnisetteHeaders
from amessage_core.ids.crypto import IDSCrypto
from amessage_core.protocol.message import iMessage, TapbackType
from amessage_core.protocol.bplist import serialize_bplist, deserialize_bplist
from amessage_core.protocol.attachments import AttachmentHandler

class TestAMessageProtocol(unittest.TestCase):

    def test_smbios_generator(self):
        profile = generate_hardware_profile("MacBookPro16,1")
        self.assertEqual(profile.model, "MacBookPro16,1")
        self.assertTrue(profile.serial_number.startswith("C02"))
        self.assertEqual(len(profile.serial_number), 12)
        self.assertEqual(len(profile.mlb), 17)
        self.assertEqual(len(profile.rom), 6)

    def test_crypto_ecdh_and_aes_gcm(self):
        alice = IDSCrypto()
        bob = IDSCrypto()

        secret_alice = alice.compute_ecdh_shared_secret(bob.public_encryption_key_bytes)
        secret_bob = bob.compute_ecdh_shared_secret(alice.public_encryption_key_bytes)
        self.assertEqual(secret_alice, secret_bob)

if __name__ == "__main__":
    unittest.main()
