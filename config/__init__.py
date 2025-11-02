import json
import os
import shutil

from .Config import Config


CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
CONFIG_EXAMPLE = os.path.join(CONFIG_DIR, "config.example.json")

if not os.path.exists(CONFIG_FILE):
    shutil.copy(CONFIG_EXAMPLE, CONFIG_FILE)
config = Config.from_dict(json.load(open(CONFIG_FILE, "r")))

DIFY_AUTHORIZATION = f"Bearer {config.dify.dify_api_key}"

__all__ = ["Config", "config", "headers"]
