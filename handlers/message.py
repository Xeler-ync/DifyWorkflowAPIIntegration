from tornado.web import RequestHandler
from models.chat import chat_manager, Message
from utils.response import APIHandler
import json
import uuid
import time
import asyncio
import random
from training.scripts.api import start_search_process


class MessageHandler(APIHandler):
    search_conn = None
    pending_responses = {}
    _initialized = False

    @classmethod
    def initialize_search(cls, pipe=None):
        if not cls._initialized:
            try:
                if not pipe:
                    cls.search_conn = start_search_process()
                else:
                    cls.search_conn = pipe
                cls._initialized = True

                # 启动响应监听线程
                import threading

                def listen_responses():
                    while True:
                        try:
                            # if cls.search_conn and cls.search_conn.poll():
                            response = cls.search_conn.recv()
                            if response and "request_id" in response:
                                cls.pending_responses[response["request_id"]] = (
                                    response
                                )
                        except Exception as e:
                            print(f"Error in response listener: {e}")
                            break

                thread = threading.Thread(target=listen_responses, daemon=True)
                thread.start()
            except Exception as e:
                print(f"Failed to initialize search process: {e}")

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        # self.__class__.initialize_search(self.search_conn)

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

            # 生成唯一的请求ID
            request_id = str(uuid.uuid4())

            # 发送搜索请求
            self.search_conn.send(
                {"type": "search", "request_id": request_id, "q": content, "k": 5}
            )

            # 等待对应的响应
            timeout = 15  # 15秒超时
            start_time = time.time()

            while request_id not in self.__class__.pending_responses:
                if time.time() - start_time > timeout:
                    self.set_status(500)
                    self.write_json({"error": "Search timeout"})
                    return
                await asyncio.sleep(0.01)  # 避免阻塞事件循环

            # 获取并移除响应
            response = self.__class__.pending_responses.pop(request_id)
            results = response.get("results", [])

            # 添加用户消息
            user_message = Message(
                username="用户",
                content=content,
                position="right",
                avatar="/fywy.gif",
            )
            session.add_message(user_message)

            # 添加AI回复（简单的echo）
            if results:
                # 随机选择一个结果
                # selected = random.choice(results)
                selected = results[0]
                ai_message = Message(
                    username="AI助手",
                    content=selected.get("answer", "抱歉，我没有找到相关答案"),
                    position="left",
                    avatar="/nwlt.jpg",
                )
            else:
                ai_message = Message(
                    username="AI助手",
                    content="抱歉，我没有找到相关答案",
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
