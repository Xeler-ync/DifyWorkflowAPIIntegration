import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import asyncio

# WebSocket 客户端连接池
websocket_clients = set()
response_queue = asyncio.Queue()


class QuestionClassifyHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket connection opened")
        websocket_clients.add(self)

    def on_message(self, message):
        print(f"Received message from client: {message}")
        # 将消息转发给 HTTP 请求处理程序
        try:
            data = json.loads(message)
            request_id = data.get("id")
            if request_id:
                self.application.http_request_processor.handle_response(
                    request_id, message
                )
        except json.JSONDecodeError:
            print("Invalid JSON message received")

    def on_close(self):
        print("WebSocket connection closed")
        websocket_clients.remove(self)

    def check_origin(self, origin):
        # 允许跨域请求
        return True
