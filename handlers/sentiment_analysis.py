import tornado.websocket
import json
import asyncio

# WebSocket 客户端连接池
websocket_clients = set()
responses = {}


class SentimentAnalysisHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket connection opened")
        websocket_clients.add(self)

    def on_message(self, message):
        print(f"Received message from client: {message}")
        try:
            data = json.loads(message)
            if request_id := data.get("id"):
                responses[request_id] = data
        except json.JSONDecodeError:
            print("Invalid JSON message received")

    def on_close(self):
        print("WebSocket connection closed")
        websocket_clients.remove(self)

    def check_origin(self, origin):
        # 允许跨域请求
        return True
