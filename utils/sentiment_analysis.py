import json
import uuid
import asyncio
from typing import List
from handlers.sentiment_analysis import websocket_clients, responses


class SentimentAnalysisUtil:

    def send_to_websocket(self, data):
        message = json.dumps(data)
        for client in websocket_clients:
            client.write_message(message)

    def handle_response(self, request_id, message):
        responses[request_id] = message

    async def process_request(self, content: str) -> List[str]:
        request_id = str(uuid.uuid4())
        data = {"content": content, "id": request_id}
        self.send_to_websocket(data)

        while request_id not in responses:
            await asyncio.sleep(0.1)
        response = responses[request_id]
        del responses[request_id]
        return response["data"]
