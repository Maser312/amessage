#!/usr/bin/env python3
import socket
import ssl
import time

HOST = "courier.push.apple.com"
PORT = 5223

def test_connection():
    print(f"Testing TLS connection to Apple APNs ({HOST}:{PORT})...")
    start_time = time.time()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.settimeout(10.0)
    try:
        sock = ctx.wrap_socket(raw_sock, server_hostname=HOST)
        sock.connect((HOST, PORT))
        elapsed = (time.time() - start_time) * 1000
        print(f"SUCCESS: Connected to Apple APNs in {elapsed:.1f}ms!")
        sock.close()
    except Exception as e:
        print(f"ERROR: Failed to connect to APNs: {e}")

if __name__ == "__main__":
    test_connection()
