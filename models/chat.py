import requests
from typing import List, Dict, Optional
from .session import ChatSession
from .message import Message
from config import config, DIFY_AUTHORIZATION


class ChatManager:
    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        has_more = True
        history = []
        while has_more:
            response = requests.get(
                f"{config.dify.dify_endpoint}/messages",
                params={"user": config.dify.user, "conversation_id": session_id},
                headers={"Authorization": DIFY_AUTHORIZATION},
            )

            data = response.json()
            his = []
            for item in data["data"]:
                his.append(
                    Message(
                        username="用户",
                        content=item["query"],
                        position="right",
                        timestamp=item["created_at"],
                        avatar="fywy.gif",
                    )
                )
                his.append(
                    Message(
                        username="AI助手",
                        content=item["answer"],
                        position="left",
                        timestamp=item["created_at"],
                        avatar="nwlt.jpg",
                    )
                )
            history.extend(his)
            has_more = data["has_more"]

        return history

    def create_session(self) -> ChatSession:
        session = ChatSession()
        welcome_msg = Message(
            username="AI助手",
            content="你好！我是AI助手，有什么可以帮助你的吗？",
            position="left",
            avatar="/nwlt.jpg",
        )
        session.add_message(welcome_msg)
        self.sessions[session.id] = session
        self.save_session(session)
        return session

    async def delete_session(self, session_id: str) -> bool:
        try:
            response = requests.delete(
                f"{config.dify.dify_endpoint}/conversations/{session_id}",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": DIFY_AUTHORIZATION,
                },
                json={"user": config.dify.user},
            )

            if response.status_code == 204:
                if session_id in self.sessions:
                    del self.sessions[session_id]
                return True
            return False
        except Exception as e:
            print(f"删除会话失败: {e}")
            return False

    def get_session_messages(self, session_id: str) -> List[Message]:
        """获取特定会话的所有消息"""
        session = self.get_session(session_id)
        if session:
            return session
        return []

    def get_all_sessions(
        self, last_id: str | None = None, limit: int = 20
    ) -> List[ChatSession]:
        response = requests.get(
            f"{config.dify.dify_endpoint}/conversations",
            params={"user": config.dify.user, "last_id": last_id, "limit": limit},
            headers={"Authorization": DIFY_AUTHORIZATION},
        )

        data = response.json()
        self.sessions = {
            item["id"]: ChatSession(
                id=item["id"],
                title=item["name"],
                created_at=int(item["created_at"] * 1000),
                updated_at=int(item["updated_at"] * 1000),
            )
            for item in data["data"]
        }
        return list(self.sessions.values())


# 全局聊天管理器实例
chat_manager = ChatManager()
