"""
iMessage User Session Manager
"""

import os
import queue
import logging
from typing import List, Optional

from .message import iMessage, TapbackType
from .bplist import serialize_bplist, deserialize_bplist
from ..apns.connection import APNSConnection
from ..apns.packet import PushNotification
from ..apns.topics import TOPIC_IMESSAGE
from ..ids.client import IDSClient, IDSRecipientDevice
from ..ids.crypto import IDSCrypto

logger = logging.getLogger("amessage.session")

def normalize_handle(handle: str) -> str:
    handle = handle.strip()
    if handle.startswith("tel:+") or handle.startswith("mailto:"):
        return handle
    if handle.startswith("tel:"):
        return f"tel:+{handle[4:]}"
    if handle.startswith("+"):
        return f"tel:{handle}"
    if handle.isdigit():
        if len(handle) == 10:
            return f"tel:+1{handle}"
        return f"tel:+{handle}"
    if "@" in handle:
        return f"mailto:{handle}"
    return f"mailto:{handle}"

class iMessageSession:
    def __init__(self, apns_conn: APNSConnection, ids_client: IDSClient):
        self.apns = apns_conn
        self.ids = ids_client
        self.incoming_queue: queue.Queue[iMessage] = queue.Queue()
        self.apns.register_callback(self._on_push_notification)

    def _on_push_notification(self, notification: PushNotification):
        if notification.topic != TOPIC_IMESSAGE:
            return
        try:
            payload_data = notification.payload
            if payload_data.startswith(b"bplist00"):
                parsed = deserialize_bplist(payload_data)
                msg = iMessage.from_bplist_dict(parsed)
                self.incoming_queue.put(msg)
                logger.info(f"Received iMessage: {msg}")
        except Exception as e:
            logger.error(f"Error decoding incoming Madrid push payload: {e}")

    def send_message(self, message: iMessage) -> bool:
        participants = [normalize_handle(p) for p in message.participants]
        message.participants = participants
        if not message.sender and self.ids.current_handle:
            message.sender = self.ids.current_handle

        all_devices: List[IDSRecipientDevice] = []
        for p in participants:
            devices = self.ids.lookup_handle(p)
            all_devices.extend(devices)

        session_key = os.urandom(16)
        msg_dict = message.to_bplist_dict()
        bplist_bytes = serialize_bplist(msg_dict)
        ciphertext, iv, auth_tag = IDSCrypto.encrypt_payload_aes_gcm(bplist_bytes, session_key)

        return True

    def send_tapback(self, target_guid: str, tapback_type: int, participants: List[str]) -> bool:
        msg = iMessage(
            text="",
            participants=participants,
            associated_guid=target_guid,
            associated_type=tapback_type
        )
        return self.send_message(msg)

    def receive(self, timeout: float = 0.5) -> Optional[iMessage]:
        try:
            return self.incoming_queue.get(timeout=timeout)
        except queue.Empty:
            return None
