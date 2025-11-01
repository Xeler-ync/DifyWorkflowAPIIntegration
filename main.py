import logging
import tornado.web
import tornado.ioloop
import tornado.autoreload
from handlers.chat import ChatListHandler, ChatDetailHandler, ChatMessagesHandler
from handlers.message import MessageHandler
from config import config


def make_app():
    # 配置日志等级
    logging.basicConfig(
        level=config.log_level,  # 可以是 DEBUG, INFO, WARNING, ERROR, CRITICAL
        # format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # 获取 Tornado 的 logger 并设置等级
    tornado.log.access_log.setLevel(config.log_level)
    tornado.log.app_log.setLevel(config.log_level)
    tornado.log.gen_log.setLevel(config.log_level)

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
    app.listen(config.port, config.address)
    print(f"Server is running on http://{config.address}:{config.port}")
    tornado.autoreload.start()  # 启动自动重载
    tornado.ioloop.IOLoop.current().start()
