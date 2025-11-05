from tornado.web import RequestHandler
from llm import get_result
from models.chat import chat_manager, Message
from typing import List, Optional
from utils.response import APIHandler
from utils.question_classify import QuestionClassifierUtil
import json

qcu: QuestionClassifierUtil = QuestionClassifierUtil()


class MessageHandler(APIHandler):
    async def post(self):
        """发送消息"""
        try:
            data = json.loads(self.request.body.decode())
            session_id = data.get("sessionId")
            content = data.get("content")

            if not session_id or not content:
                self.set_status(400)
                self.write_json({"error": "Missing sessionId or content"})
                return

            session = chat_manager.get_session(session_id)
            if not session:
                self.set_status(404)
                self.write_json({"error": "Session not found"})
                return

            # 添加用户消息
            user_message = Message(
                username="用户",
                content=content,
                position="right",
                avatar="/fywy.gif",
            )
            session.add_message(user_message)

            user_message_types = await qcu.process_request(content)

            for type in user_message_types:
                session.add_repository_type(type)

            # 添加AI回复
            ai_message = Message(
                username="AI助手",
                content=get_result(
                    messages=session.messages, repository_types=session.repository_types
                ),
                position="left",
                avatar="/nwlt.jpg",
            )
            session.add_message(ai_message)
            # 保存会话
            await chat_manager.save_session(session)

            self.write_json({"message": ai_message.to_dict()})

        except json.JSONDecodeError:
            self.set_status(400)
            self.write_json({"error": "Invalid JSON"})
        except Exception as e:
            self.set_status(500)
            self.write_json({"error": str(e)})
