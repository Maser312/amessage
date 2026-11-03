# AMessage for Windows 🪟🍏

**Native Desktop iMessage Client & Protocol Debugger for Windows**

AMessage Windows is designed for fast desktop communication, protocol testing, and live debugging of the reverse-engineered iMessage stack on PC without needing an Android emulator or device.

## 🌟 Features
- **macOS / iOS Inspired UI**: Clean desktop interface built with modern dark/light mode support (via `customtkinter`), authentic Apple blue bubbles, and tapback reaction overlays.
- **Protocol Debugger Panel**:
  - Live **APNs Packet Log** (`courier.push.apple.com:5223` socket events, pings, push deliveries)
  - **IDS Key Inspector**: View local NIST P-256 ECDH keys, peer public keys, and AES-GCM session tokens
  - **SMBIOS & Anisette Attestation Inspector**: Inspect generated Serial Number, MLB, ROM, and Board-ID
- **Instant Testing & Simulation**:
  - Send and receive real iMessages to/from any iPhone
  - Send Tapback reactions (❤️, 👍, 👎, 😂, ‼️, ❓)
  - Toggle real-time typing indicators

## 🚀 Running on Windows
Double-click `run.bat` or run:
```powershell
cd windows
pip install -r requirements.txt
python -m amessage_windows.app
```
