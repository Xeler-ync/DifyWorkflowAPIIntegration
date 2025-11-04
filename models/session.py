import uuid
from datetime import datetime
from typing import List, Set
from .message import Message
from llm import RepositoryType


class ChatSession:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.title = "新对话"
        self.messages: List[Message] = []
        self.created_at = datetime.now().timestamp()
        self.updated_at = datetime.now().timestamp()
        self.repository_types: Set[RepositoryType] = set()

    def add_message(self, message: Message):
        self.messages.append(message)
        self.updated_at = int(datetime.now().timestamp() * 1000)
        if len(self.messages) == 2:  # 第一条用户消息后更新标题
            self.title = message.content[:20] + (
                "..." if len(message.content) > 20 else ""
            )

    def add_repository_type(self, repository_type: RepositoryType):
        self.repository_types.add(repository_type)

    @classmethod
    def from_dict(cls, data: dict) -> "ChatSession":
        session = cls()
        session.id = data["id"]
        session.title = data["title"]
        session.created_at = data["createdAt"]
        session.updated_at = data["updatedAt"]
        session.messages = [Message.from_dict(msg) for msg in data["messages"]]
        session.repository_types = data["repositoryTypes"]
        return session

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "messages": [msg.to_dict() for msg in self.messages],
            "repositoryTypes": self.repository_types,
        }
