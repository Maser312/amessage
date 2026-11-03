# iMessage Protocol Reverse-Engineering Architecture

This document provides a comprehensive technical breakdown of Apple's iMessage protocol stack, based on reverse engineering of macOS (IMCore, IMFoundation, identityservicesd, apsd) and open-source protocol research (pypush, rustpush, OpenBubbles).

---

## 1. The Protocol Stack Overview

Unlike modern web chat apps that use WebSockets or gRPC over HTTPS, iMessage is built upon a hybrid stack:

```
+-------------------------------------------------------------+
|                      Application Layer                      |
|         iMessage Payloads, Tapbacks, Typing, MMCS Media     |
|                      (Binary Plist / XML)                   |
+-------------------------------------------------------------+
|                      Encryption Layer                       |
|           NIST P-256 ECDH + AES-128-GCM / AES-CTR           |
+-------------------------------------------------------------+
|                   Identity Services (IDS)                   |
|       service.ess.apple.com / Device Directory Lookup       |
+-------------------------------------------------------------+
|            Apple Push Notification service (APNs)           |
|         courier.push.apple.com:5223 / Raw TLS Packet        |
+-------------------------------------------------------------+
|                      Transport (TCP/TLS)                    |
+-------------------------------------------------------------+
```
