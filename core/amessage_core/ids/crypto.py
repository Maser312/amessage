"""
Cryptographic Primitives for iMessage / IDS
- NIST P-256 (secp256r1) ECDH and ECDSA
- AES-128 / AES-256 GCM and CTR
- RSA-2048 identity fallback
- HKDF key derivation
"""

import os
from base64 import b64encode, b64decode
from typing import Tuple

from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class KeyPair:
    def __init__(self, private_pem: str, cert_der_b64: str = ""):
        self.private_pem = private_pem
        self.cert_der_b64 = cert_der_b64

class IDSCrypto:
    def __init__(self):
        self.ec_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        self.ec_signing_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        self.rsa_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

    def export_keys(self) -> dict:
        ec_priv_bytes = self.ec_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode("utf-8")

        ec_sign_bytes = self.ec_signing_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode("utf-8")

        rsa_priv_bytes = self.rsa_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode("utf-8")

        return {
            "ec_encryption_key": ec_priv_bytes,
            "ec_signing_key": ec_sign_bytes,
            "rsa_key": rsa_priv_bytes
        }

    @property
    def public_encryption_key_bytes(self) -> bytes:
        return self.ec_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    @property
    def public_signing_key_bytes(self) -> bytes:
        return self.ec_signing_key.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    @property
    def public_rsa_key_bytes(self) -> bytes:
        return self.rsa_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.PKCS1
        )

    def compute_ecdh_shared_secret(self, peer_public_der: bytes) -> bytes:
        peer_pub = serialization.load_der_public_key(peer_public_der, backend=default_backend())
        return self.ec_private_key.exchange(ec.ECDH(), peer_pub)

    @staticmethod
    def encrypt_payload_aes_gcm(plaintext: bytes, key: bytes) -> Tuple[bytes, bytes, bytes]:
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return ciphertext, iv, encryptor.tag

    @staticmethod
    def decrypt_payload_aes_gcm(ciphertext: bytes, key: bytes, iv: bytes, tag: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    @staticmethod
    def encrypt_payload_aes_ctr(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(plaintext) + encryptor.finalize()

    @staticmethod
    def decrypt_payload_aes_ctr(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
