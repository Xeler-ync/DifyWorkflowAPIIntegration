import asyncio
import websockets
import json
from config import config
from question_classify import get_top_n_predictions, clf, vectorizer


async def websocket_client():
    uri = f"ws://localhost:{config.port}/api/question_classify"
    retry_delay = 2  # 秒
    retry_count = 0

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("连接成功！")
                retry_count = 0  # 重置重试计数器

                while True:
                    try:
                        # 接收服务器发送的消息
                        message = await websocket.recv()
                        print(f"收到消息：{message}")

                        # 解析 JSON 消息
                        data = json.loads(message)
                        print("解析 JSON 消息")

                        # 处理消息
                        response_data = {
                            "id": data["id"],
                            "status": "success",
                            "data": get_top_n_predictions(
                                data["content"], clf, vectorizer, 3
                            ),
                        }
                        # response_data["data"] is List[str], where str is filename
                        print("处理消息")

                        # 将处理后的消息发送回服务器
                        response_message = json.dumps(response_data)
                        print("处理处理后的消息")
                        await websocket.send(response_message)
                        print(f"发送响应：{response_message}")
                    except websockets.exceptions.ConnectionClosed as e:
                        print(f"连接已关闭, {e.reason}")
                        break

        except Exception as e:
            retry_count += 1
            print(f"连接失败, {e}, {retry_delay}秒后重试... (尝试 {retry_count})")
            await asyncio.sleep(retry_delay)


# 运行客户端
asyncio.run(websocket_client())
