"""
APNs Binary Packet Parser and Serializer
"""

import struct
from typing import Dict, Any, List, Optional

CMD_CONNECT = 0x01
CMD_CONNECT_ACK = 0x02
CMD_FILTER = 0x07
CMD_PING = 0x08
CMD_PING_ACK = 0x09
CMD_NOTIFICATION = 0x0A
CMD_NOTIFICATION_ACK = 0x0B
CMD_ERROR = 0x0C

class APNSPacket:
    def __init__(self, command: int, payload: bytes = b""):
        self.command = command
        self.payload = payload

    def serialize(self) -> bytes:
        length = len(self.payload)
        return struct.pack("!BI", self.command, length) + self.payload

class FilterPacket(APNSPacket):
    def __init__(self, topics: List[str]):
        payload = bytearray()
        for topic in topics:
            topic_bytes = topic.encode("utf-8")
            payload.extend(struct.pack("!H", len(topic_bytes)))
            payload.extend(topic_bytes)
        super().__init__(CMD_FILTER, bytes(payload))

class PingPacket(APNSPacket):
    def __init__(self):
        super().__init__(CMD_PING, b"")

class NotificationAckPacket(APNSPacket):
    def __init__(self, message_id: int):
        payload = struct.pack("!I", message_id)
        super().__init__(CMD_NOTIFICATION_ACK, payload)

class PushNotification:
    def __init__(self, topic: str, token: bytes, payload: bytes, message_id: int = 0):
        self.topic = topic
        self.token = token
        self.payload = payload
        self.message_id = message_id

    @classmethod
    def parse(cls, data: bytes) -> Optional["PushNotification"]:
        try:
            offset = 0
            topic = ""
            token = b""
            payload = b""
            msg_id = 0

            while offset < len(data):
                if offset + 3 > len(data):
                    break
                item_id, item_len = struct.unpack("!BH", data[offset:offset+3])
                offset += 3
                item_data = data[offset:offset+item_len]
                offset += item_len

                if item_id == 1:
                    token = item_data
                elif item_id == 2:
                    topic = item_data.decode("utf-8", errors="ignore")
                elif item_id == 3:
                    payload = item_data
                elif item_id == 4:
                    if len(item_data) >= 4:
                        msg_id = struct.unpack("!I", item_data[:4])[0]

            return cls(topic=topic, token=token, payload=payload, message_id=msg_id)
        except Exception:
            return None
