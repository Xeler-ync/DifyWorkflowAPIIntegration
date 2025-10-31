import asyncio
from typing import List, Dict, Optional
from .session import ChatSession
from .message import Message
from .database import Database


class ChatManager:
    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}
        self.db = Database()
        asyncio.run(self.load_data())

    async def load_data(self):
        """从JSON文件加载聊天数据"""
        try:
            sessions_data = await self.db.load_all_sessions()
            for session_data in sessions_data:
                session = ChatSession.from_dict(session_data)
                self.sessions[session.id] = session
        except Exception as e:
            print(f"加载数据失败: {e}")

    async def save_session(self, session: ChatSession):
        """保存会话到JSON文件"""
        try:
            await self.db.save_session(session.id, session.to_dict())
        except Exception as e:
            print(f"保存会话失败: {e}")

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        return self.sessions.get(session_id)

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
        if session_id in self.sessions:
            try:
                await self.db.delete_session(session_id)
                del self.sessions[session_id]
                return True
            except Exception as e:
                print(f"删除会话失败: {e}")
        return False

    def get_session_messages(self, session_id: str) -> List[Message]:
        """获取特定会话的所有消息"""
        session = self.get_session(session_id)
        if session:
            return session.messages
        return []

    def get_all_sessions(self) -> List[ChatSession]:
        return list(self.sessions.values())


# 全局聊天管理器实例
chat_manager = ChatManager()
