"""
AMessage Headless Validation & Anisette Relay Server
Provides hardware attestation endpoints for Android devices without Apple hardware.
"""

import os
import time
import base64
import hashlib
from flask import Flask, jsonify, request
from mac_generator import generate_mac_profile

app = Flask(__name__)
PROFILE = generate_mac_profile()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "amessage-relay",
        "profile": PROFILE["model"]
    })

@app.route("/api/v1/bridge/get-version-info", methods=["POST", "GET"])
def get_version_info():
    return jsonify({
        "versions": {
            "software_build_id": "22G513",
            "software_name": "macOS",
            "software_version": "13.6.4",
            "serial_number": PROFILE["serial_number"],
            "hardware_version": PROFILE["model"],
            "unique_device_id": PROFILE["platform_uuid"]
        }
    })

@app.route("/api/v1/bridge/get-validation-data", methods=["POST"])
def get_validation_data():
    timestamp = int(time.time())
    seed = f"{PROFILE['serial_number']}:{PROFILE['mlb']}:{timestamp}".encode("utf-8")
    validation_bytes = hashlib.sha256(seed).digest() + bytes.fromhex(PROFILE["rom"])
    b64_data = base64.b64encode(validation_bytes).decode("utf-8")
    return jsonify({"data": b64_data})

@app.route("/api/v1/anisette/headers", methods=["GET"])
def get_anisette_headers():
    timestamp = int(time.time())
    seed = f"{PROFILE['serial_number']}:{PROFILE['mlb']}:{timestamp}".encode("utf-8")
    otp_hash = hashlib.sha256(seed).digest()
    x_apple_md = base64.b64encode(otp_hash[:16]).decode("utf-8")

    m_seed = f"{PROFILE['platform_uuid']}:{PROFILE['board_id']}".encode("utf-8")
    x_apple_md_m = base64.b64encode(hashlib.sha256(m_seed).digest()[:16]).decode("utf-8")

    return jsonify({
        "X-Apple-I-MD": x_apple_md,
        "X-Apple-I-MD-M": x_apple_md_m,
        "X-Apple-I-MD-RINFO": "17106176",
        "X-Apple-I-MD-LU": "0",
        "X-Apple-I-SRL-NO": PROFILE["serial_number"],
        "X-Apple-I-Client-Time": str(timestamp),
        "User-Agent": f"iMessage/13.0 ({PROFILE['model']}; macOS 13.6.4)"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
