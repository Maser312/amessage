# AMessage Android Client

Native Android client for AMessage, written in **Kotlin** with **Jetpack Compose** and Material 3 design, mirroring the authentic Apple iMessage experience (blue bubbles, tapback reactions, typing indicators, delivery timestamps).

## Architecture
- **UI**: Jetpack Compose with responsive iMessage aesthetic.
- **Service**: Foreground `APNsService` maintaining persistent socket connection to Apple Push Gateway.
- **Cryptographic Engine**: Local NIST P-256 ECDH and AES-GCM encryption/decryption keys generated and stored in Android Keystore.
- **Relay Bridge**: Integrated settings for connecting to self-hosted or community relays.
