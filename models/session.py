import uuid
from datetime import datetime
from typing import Optional
from .message import Message


class ChatSession:
    def __init__(
        self,
        id: Optional[str],
        title: Optional[str],
        created_at: Optional[float],
        updated_at: Optional[float],
    ):
        self.id = id or str(uuid.uuid4())
        self.title = title or "新对话"
        self.created_at = created_at or datetime.now().timestamp()
        self.updated_at = updated_at or datetime.now().timestamp()

    @classmethod
    def from_dict(cls, data: dict) -> "ChatSession":
        session = cls()
        session.id = data["id"]
        session.title = data["title"]
        session.created_at = data["createdAt"]
        session.updated_at = data["updatedAt"]
        return session

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }
