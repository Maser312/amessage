"""
APNs Connection Manager - Direct TLS connection to Apple Push Notification Service
"""

import ssl
import socket
import struct
import threading
import time
import logging
from typing import List, Callable, Optional
from base64 import b64encode, b64decode

from .packet import APNSPacket, FilterPacket, PingPacket, NotificationAckPacket, PushNotification, CMD_NOTIFICATION, CMD_PING_ACK
from .topics import DEFAULT_TOPICS, TOPIC_IMESSAGE

logger = logging.getLogger("amessage.apns")

COURIER_SERVERS = [
    "courier.push.apple.com",
    "1-courier.push.apple.com",
    "2-courier.push.apple.com",
    "3-courier.push.apple.com",
    "4-courier.push.apple.com",
    "5-courier.push.apple.com"
]
DEFAULT_PORT = 5223
FALLBACK_PORT = 443

class APNSConnection:
    def __init__(self, client_key: Optional[str] = None, client_cert: Optional[str] = None):
        self.client_key = client_key
        self.client_cert = client_cert
        self.sock: Optional[ssl.SSLSocket] = None
        self.is_connected = False
        self.token: Optional[bytes] = None
        self.callbacks: List[Callable[[PushNotification], None]] = []
        self._running = False
        self._listener_thread: Optional[threading.Thread] = None
        self._ping_thread: Optional[threading.Thread] = None

    def register_callback(self, cb: Callable[[PushNotification], None]):
        self.callbacks.append(cb)

    def connect(self, token: Optional[bytes] = None, host: Optional[str] = None, port: int = DEFAULT_PORT):
        if host is None:
            host = COURIER_SERVERS[0]
        
        self.token = token
        logger.info(f"Connecting to APNs gateway at {host}:{port}...")

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_sock.settimeout(30.0)

        try:
            self.sock = context.wrap_socket(raw_sock, server_hostname=host)
            self.sock.connect((host, port))
            self.is_connected = True
            self._running = True
            logger.info("Connected securely to Apple Push Gateway.")

            self._listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self._listener_thread.start()

            self._ping_thread = threading.Thread(target=self._keepalive_loop, daemon=True)
            self._ping_thread.start()

            self.filter(DEFAULT_TOPICS)

        except Exception as e:
            logger.error(f"Failed to connect to APNs: {e}")
            self.is_connected = False
            raise

    def filter(self, topics: List[str]):
        if not self.is_connected or not self.sock:
            return
        pkt = FilterPacket(topics)
        self.send_packet(pkt)
        logger.info(f"Subscribed to APNs topics: {topics}")

    def send_packet(self, pkt: APNSPacket):
        if not self.sock:
            return
        try:
            data = pkt.serialize()
            self.sock.sendall(data)
        except Exception as e:
            logger.error(f"Error sending APNs packet: {e}")
            self.is_connected = False

    def _listen_loop(self):
        while self._running and self.is_connected and self.sock:
            try:
                header = self._read_bytes(5)
                if not header:
                    break
                cmd, length = struct.unpack("!BI", header)
                payload = self._read_bytes(length) if length > 0 else b""

                if cmd == CMD_NOTIFICATION:
                    notification = PushNotification.parse(payload)
                    if notification:
                        logger.info(f"Received push notification for topic: {notification.topic}")
                        if notification.message_id:
                            self.send_packet(NotificationAckPacket(notification.message_id))
                        for cb in self.callbacks:
                            try:
                                cb(notification)
                            except Exception as ex:
                                logger.error(f"Callback error processing push: {ex}")

                elif cmd == CMD_PING_ACK:
                    logger.debug("Received APNs ping pong ack.")

            except Exception as e:
                logger.warning(f"APNs socket exception: {e}")
                break

        self.is_connected = False
        logger.info("APNs connection closed.")

    def _read_bytes(self, num_bytes: int) -> bytes:
        data = bytearray()
        while len(data) < num_bytes and self._running:
            chunk = self.sock.recv(num_bytes - len(data))
            if not chunk:
                return bytes(data)
            data.extend(chunk)
        return bytes(data)

    def _keepalive_loop(self):
        while self._running and self.is_connected:
            time.sleep(120)
            if self.is_connected:
                self.send_packet(PingPacket())

    def close(self):
        self._running = False
        self.is_connected = False
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
