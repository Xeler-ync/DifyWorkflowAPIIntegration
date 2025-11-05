import json
import uuid
import asyncio
from typing import List
from handlers.question_classify import websocket_clients, responses
from llm import RepositoryType


class QuestionClassifierUtil:
    # def __init__(self):
    #     self.loop = asyncio.get_event_loop()

    def send_to_websocket(self, data):
        message = json.dumps(data)
        for client in websocket_clients:
            client.write_message(message)

    def handle_response(self, request_id, message):
        responses[request_id] = message

    async def process_request(self, content: str) -> List[str]:
        request_id = str(uuid.uuid4())  # 生成唯一的请求 ID
        data = {"content": content, "id": request_id}
        self.send_to_websocket(data)
        # 等待 WebSocket 客户端的响应
        while request_id not in responses:
            await asyncio.sleep(0.1)
        response = responses[request_id]
        del responses[request_id]  # 清理响应
        return response["data"]
