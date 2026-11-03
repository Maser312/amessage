# AMessage Core Protocol Engine

`amessage-core` is the Python implementation of the reverse-engineered iMessage protocol. It handles:
- **APNs**: TLS client socket to `courier.push.apple.com:5223`
- **IDS**: Identity registration, public key directory lookup (`lookup-handle`), Apple ID authentication
- **Anisette & Validation**: Client for remote validation relay or OpenCore SMBIOS spoofing
- **E2EE**: NIST P-256 (secp256r1) key agreement, AES-GCM/CTR payload encryption & decryption
- **iMessage Messaging**: Text messages, tapback reactions, typing indicators, read receipts, attachments

## CLI Usage

```bash
pip install -r requirements.txt
python -m amessage_core.cli
```
