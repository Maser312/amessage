# AMessage 🍏💬

**Native iMessage Client for Android & Windows — 100% Apple-Hardware-Free**

AMessage is an open-source, reverse-engineered implementation of Apple's iMessage protocol designed to run natively on Android and Windows. It allows non-Apple users to communicate directly with iPhone users using authentic blue bubbles, full end-to-end encryption (E2EE), read receipts, typing indicators, high-resolution media attachments, and tapback reactions — **without requiring the user to own or buy any Apple devices**.

---

## 🌟 Key Highlights

- **No Apple Hardware Required**: Connects to iMessage without owning an iPhone, Mac, or iPad.
- **Cross-Platform (Android & Windows)**:
  - **Android Client**: Native Jetpack Compose app with background APNs push keepalive.
  - **Windows Desktop & Debugger**: Full desktop app with protocol inspector for live debugging.
- **Direct Apple Connection**: Connects straight to Apple's Push Notification service (`courier.push.apple.com`) and Identity Services (IDS) via TLS. Messages are end-to-end encrypted (E2EE) on your device using NIST P-256 ECDH and AES-GCM.
- **Full iMessage Protocol Support**:
  - Blue bubbles with delivery & read receipts
  - Real-time typing indicators
  - Tapback reactions (Love, Like, Dislike, Laugh, Exclaim, Question)
  - Full-resolution photos, videos, and audio notes via Apple MMCS (MobileMe Cloud Services)
  - Group chats & handle routing (Email or Phone number)
- **Flexible Hardware Validation Modes**:
  - **Community Relay Mode**: Connect via decentralized validation relays (OpenBubbles / Beeper-compatible).
  - **Self-Hosted Virtual Mac Relay**: Run a 1-click Docker container (`amessage-relay` / Docker-OSX) on any cheap Linux VPS, local PC, or free cloud tier.
  - **Emulated ADI/NAC**: Integrated CPU emulation fallback using valid OpenCore-generated SMBIOS hardware signatures.

---

## 🏗️ System Architecture

```
+-------------------------------------------------------------------+
|                   Client Device (Android or Windows)              |
|                                                                   |
|  +--------------------+         +------------------------------+  |
|  | Modern Desktop UI  | <-----> |   AMessage Protocol Core     |  |
|  | (Compose / WinUI)  |         | (APNs, IDS, E2EE, MMCS Sync) |  |
|  +--------------------+         +------------------------------+  |
|                                     |                     ^       |
+-------------------------------------|---------------------|-------+
                                      |                     |
           (Direct E2EE Push Messages)|        (Validation  |
                     Port 5223 / TLS  |         Tokens Only)|
                                      v                     |
              +----------------------------+                |
              |   Apple APNs & IDS Cloud   |                |
              | (courier.push.apple.com)   |                |
              | (service.ess.apple.com)    |                |
              +----------------------------+                |
                            ^                               |
                            |                               v
           +------------------------------------------------------+
           |       Validation Relay / Headless Virtual Mac        |
           |             (amessage-relay or Docker-OSX)           |
           |     * Signs initial registration / Anisette only     |
           |     * NEVER sees messages or private keys            |
           +------------------------------------------------------+
```

For an in-depth breakdown of the protocol, see [ARCHITECTURE.md](ARCHITECTURE.md).  
For the technical guide on bypassing Apple hardware restrictions, see [HACKS_AND_BYPASSES.md](HACKS_AND_BYPASSES.md).

---

## 🚀 Getting Started

### Option 1: Running on Windows (Fast Protocol Debugger & Desktop App)

Launch the desktop client with live packet inspector:
```powershell
cd windows
pip install -r requirements.txt
python -m amessage_windows.app
```
Or simply double-click `windows/run.bat`.

### Option 2: Quick CLI Test (Core Protocol)

Run the Python protocol core directly on your computer or Android (via Termux):

```bash
git clone https://github.com/Maser312/amessage.git
cd amessage/core
pip install -r requirements.txt
python -m amessage_core.cli
```

### Option 3: Deploying the Headless Relay (Docker)

If you don't own an Apple device, launch the self-hosted relay on any Linux server, Windows PC (WSL2), or Docker host:

```bash
cd relay
docker compose up -d
```

### Option 4: Building the Android App

```bash
cd client
./gradlew assembleDebug
```

---

## 🔐 Security & Privacy

1. **End-to-End Encryption**: All messages, attachments, and metadata are encrypted on your local device using Apple's native cryptographic algorithms (P-256 ECDH + AES-128-GCM). Only the intended recipient can decrypt your messages.
2. **Zero-Knowledge Relay**: The validation relay is used **strictly during initial authentication** to generate Anisette and Validation Data tokens (`X-Apple-I-MD`, `X-Apple-ActionSignature`). The relay **never** receives your private keys, Apple ID password, or message contents.
3. **No Centralized Intermediary**: Unlike web-relayed solutions that forward chat logs through a third-party server, AMessage maintains a direct TLS socket connection to Apple's push infrastructure.

---

## 📜 Documentation

- [iMessage Protocol Architecture](ARCHITECTURE.md)
- [Hardware Spoofing & Bypass Deep Dive](HACKS_AND_BYPASSES.md)
- [Windows Client & Debugger Guide](windows/README.md)
- [Android Client Guide](client/README.md)
- [Core Engine Guide](core/README.md)
- [Relay Server Setup](relay/README.md)

---

## ⚖️ Disclaimer & Legal Notice

This project is created for educational, interoperability, and reverse-engineering research purposes under fair use doctrine and reverse engineering provisions (such as the US DMCA § 1201(f) interoperability exemption and EU Directive 2009/24/EC). 

iMessage, Apple, macOS, iOS, and iCloud are trademarks of Apple Inc. AMessage is not affiliated with, endorsed by, or sponsored by Apple Inc.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
