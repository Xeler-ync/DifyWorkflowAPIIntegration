import logging
import tornado.web
import tornado.ioloop
import tornado.autoreload
from handlers.chat import ChatListHandler, ChatDetailHandler, ChatMessagesHandler
from handlers.message import MessageHandler


def make_app():
    # 配置日志等级
    logging.basicConfig(
        level=logging.DEBUG,  # 可以是 DEBUG, INFO, WARNING, ERROR, CRITICAL
        # format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # 获取 Tornado 的 logger 并设置等级
    tornado.log.access_log.setLevel(logging.DEBUG)
    tornado.log.app_log.setLevel(logging.DEBUG)
    tornado.log.gen_log.setLevel(logging.DEBUG)

    return tornado.web.Application(
        [
            (r"/api/chats", ChatListHandler),
            (r"/api/chats/([^/]+)", ChatDetailHandler),
            (r"/api/chats/([^/]+)/messages", ChatMessagesHandler),
            (r"/api/messages", MessageHandler),
        ],
        debug=True,  # 开启调试模式
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(3000, '0.0.0.0')
    print("Server is running on http://localhost:3000")
    tornado.autoreload.start()  # 启动自动重载
    tornado.ioloop.IOLoop.current().start()
