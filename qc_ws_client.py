import asyncio
import websockets
import json
from config import config
from llm import types
from question_classify import get_top_n_predictions


async def websocket_client():
    uri = f"ws://localhost:{config.port}/question_classify"  # 替换为实际的 WebSocket 服务器地址

    async with websockets.connect(uri) as websocket:
        print("连接成功！")

        while True:
            try:
                # 接收服务器发送的消息
                message = await websocket.recv()
                print(f"收到消息：{message}")

                # 解析 JSON 消息
                data = json.loads(message)

                # 处理消息
                response_data = {
                    "id": data["id"],  # 保留原始请求 ID
                    "status": "success",
                    "data": data["message"].upper(),  # 示例处理：将消息内容转换为大写
                }

                # 将处理后的消息发送回服务器
                response_message = json.dumps(response_data)
                await websocket.send(response_message)
                print(f"发送响应：{response_message}")
            except websockets.exceptions.ConnectionClosed:
                print("连接已关闭")
                break


# 运行客户端
asyncio.run(websocket_client())
