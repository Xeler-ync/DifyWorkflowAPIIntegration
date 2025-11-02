import uuid
from datetime import datetime
from typing import Optional


class Message:
    def __init__(
        self,
        username: str,
        content: str,
        position: str,
        timestamp: int = None,
        avatar: Optional[str] = None,
    ):
        self.id = str(uuid.uuid4())
        self.username = username
        self.content = content
        self.position = position
        self.timestamp = timestamp or int(datetime.now().timestamp() * 1000)
        self.avatar = avatar or "/favicon.ico"

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        message = cls(
            username=data["username"],
            content=data["content"],
            position=data["position"],
            avatar=data["avatar"],
        )
        message.timestamp = data["timestamp"]
        return message

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "content": self.content,
            "position": self.position,
            "avatar": self.avatar,
            "timestamp": self.timestamp,
        }
