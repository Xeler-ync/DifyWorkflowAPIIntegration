import json
from tornado.web import RequestHandler


class APIHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE")

    def prepare(self):
        username = self.request.headers.get("username")
        if not username:
            self.set_status(401)
            self.write({"error": "Missing username"})
            self.finish()
            return
        self.username = username

    def options(self):
        self.set_status(204)
        self.finish()

    def write_json(self, data):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(data))

    def write_error(self, status_code, **kwargs):
        error_message = {
            "error": str(kwargs.get("exc_info", [None, "Unknown error"])[1])
        }
        self.set_status(status_code)
        self.write_json(error_message)
