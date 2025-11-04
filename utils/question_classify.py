import json
import uuid
import asyncio
from handlers.question_classify import websocket_clients


class QuestionClassifierUtil:
    def __init__(self):
        self.responses = {}
        self.loop = asyncio.get_event_loop()

    def send_to_websocket(self, data):
        message = json.dumps(data)
        for client in websocket_clients:
            client.write_message(message)

    def handle_response(self, request_id, message):
        self.responses[request_id] = message

    async def process_request(self, content: str):
        request_id = str(uuid.uuid4())  # 生成唯一的请求 ID
        data = {"content": content, "id": request_id}
        self.send_to_websocket(data)
        # 等待 WebSocket 客户端的响应
        while request_id not in self.responses:
            await asyncio.sleep(0.1)
        response = self.responses[request_id]
        del self.responses[request_id]  # 清理响应
        return response
