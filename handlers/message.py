from tornado.web import RequestHandler
from models.chat import chat_manager, Message
from utils.response import APIHandler
import json
import requests
from config import config, DIFY_AUTHORIZATION


class MessageHandler(APIHandler):
    async def post(self):
        """发送消息"""
        try:
            data = json.loads(self.request.body.decode())
            session_id = data.get("sessionId", "")
            content = data.get("content")

            if not content:
                self.set_status(400)
                self.write_json({"error": "Missing content"})
                return

            response = requests.post(
                f"{config.dify.dify_endpoint}/chat-messages",
                json={
                    "inputs": {},
                    "user": config.dify.user,
                    "conversation_id": session_id,
                    "query": content,
                    "response_mode": "blocking",
                    "files": [],
                },
                headers={
                    "Authorization": DIFY_AUTHORIZATION,
                    "Content-Type": "application/json",
                },
            )

            data = response.json()

            session_id = data.get("conversation_id")

            # 添加AI回复
            ai_message = Message(
                username="AI助手",
                content=data.get("answer"),
                position="left",
                avatar="/nwlt.jpg",
            )

            self.write_json({"sessionId": session_id, "message": ai_message.to_dict()})

        except json.JSONDecodeError:
            self.set_status(400)
            self.write_json({"error": "Invalid JSON"})
        except Exception as e:
            self.set_status(500)
            self.write_json({"error": str(e)})
