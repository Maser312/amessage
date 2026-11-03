# AMessage Headless Validation Relay

The AMessage Validation Relay is a lightweight microservice designed to run in Docker or on any Linux VPS / cloud server.

## Features
- Generates valid Apple SMBIOS profiles (MacBookPro16,1, iMac19,1, etc.)
- Provides dynamic Anisette headers (X-Apple-I-MD, X-Apple-I-MD-M)
- Provides dynamic Validation Data (NAC) required for Apple IDS registration
- Fully compatible with the OpenBubbles / Beeper bridge relay protocol specification

## Running with Docker

```bash
docker build -t amessage-relay .
docker run -d -p 8080:8080 --name amessage-relay amessage-relay
```
