from utils.response import APIHandler
from models.chat import chat_manager


class ChatListHandler(APIHandler):
    async def get(self):
        """获取所有聊天会话"""
        sessions = chat_manager.get_all_sessions()
        self.write_json([session.to_dict() for session in sessions])

    async def post(self):
        """创建新的聊天会话"""
        session = await chat_manager.create_session()
        self.write_json(
            {"sessionId": session.id, "message": session.messages[0].to_dict()}
        )


class ChatDetailHandler(APIHandler):
    async def get(self, session_id):
        """获取特定会话的消息历史"""
        session = await chat_manager.get_session(session_id)
        if not session:
            self.set_status(404)
            return
        self.write_json([msg.to_dict() for msg in session.messages])

    async def delete(self, session_id):
        """删除聊天会话"""
        if await chat_manager.delete_session(session_id):
            self.write_json({"success": True})  # 返回成功状态
        else:
            self.set_status(404)
            self.write_json({"success": False, "error": "Session not found"})


class ChatMessagesHandler(APIHandler):
    async def get(self, session_id):
        """获取特定会话的消息历史"""
        messages = chat_manager.get_session_messages(session_id)
        self.write_json([msg.to_dict() for msg in messages])
