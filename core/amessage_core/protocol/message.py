"""
iMessage Message Model, Tapbacks, and Effects
"""

import uuid
import time
from typing import List, Optional, Dict, Any

class TapbackType:
    HEART = 2000
    LIKE = 2001
    DISLIKE = 2002
    LAUGH = 2003
    EXCLAIM = 2004
    QUESTION = 2005

    EMOJI_MAP = {
        HEART: "❤️",
        LIKE: "👍",
        DISLIKE: "👎",
        LAUGH: "😂",
        EXCLAIM: "‼️",
        QUESTION: "❓"
    }

class iMessage:
    def __init__(
        self,
        text: str,
        participants: List[str],
        sender: Optional[str] = None,
        guid: Optional[str] = None,
        timestamp: Optional[float] = None,
        associated_guid: Optional[str] = None,
        associated_type: Optional[int] = None,
        effect: Optional[str] = None,
        attachments: Optional[List[dict]] = None
    ):
        self.text = text
        self.participants = participants
        self.sender = sender or ""
        self.guid = guid or str(uuid.uuid4()).upper()
        self.timestamp = timestamp or time.time()
        self.associated_guid = associated_guid
        self.associated_type = associated_type
        self.effect = effect
        self.attachments = attachments or []

    @property
    def is_tapback(self) -> bool:
        return self.associated_guid is not None and self.associated_type is not None

    def to_bplist_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "v": 1,
            "t": self.text,
            "s": self.sender,
            "p": self.participants,
            "d": self.timestamp,
            "guid": self.guid
        }
        if self.associated_guid:
            data["amg"] = self.associated_guid
            data["amt"] = self.associated_type
        if self.effect:
            data["e"] = self.effect
        if self.attachments:
            data["att"] = self.attachments
        return data

    @classmethod
    def from_bplist_dict(cls, data: Dict[str, Any]) -> "iMessage":
        return cls(
            text=data.get("t", ""),
            participants=data.get("p", []),
            sender=data.get("s", ""),
            guid=data.get("guid", str(uuid.uuid4()).upper()),
            timestamp=data.get("d", time.time()),
            associated_guid=data.get("amg"),
            associated_type=data.get("amt"),
            effect=data.get("e"),
            attachments=data.get("att", [])
        )
