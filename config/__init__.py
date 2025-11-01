import json
import logging
import os
import shutil


class Config:
    def __init__(
        self, address: str = "0.0.0.0", port: int = 54798, log_level: str = "WARNING"
    ):
        self.address = address
        self.port = port
        self.log_level = getattr(logging, log_level, logging.INFO)

    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(
            address=config_dict.get("address", "0.0.0.0"),
            port=config_dict.get("port", 54798),
            log_level=config_dict.get("log_level", "WARNING"),
        )

    def to_dict(self) -> dict:
        return {"address": self.address, "port": self.port, "log_level": self.log_level}

    def __str__(self) -> str:
        return f"Config(address='{self.address}', port={self.port}, log_level='{self.log_level})"

    def __repr__(self) -> str:
        return self.__str__()


CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
CONFIG_EXAMPLE = os.path.join(CONFIG_DIR, "config.example.json")

if not os.path.exists(CONFIG_FILE):
    shutil.copy(CONFIG_EXAMPLE, CONFIG_FILE)
config = Config.from_dict(json.load(open(CONFIG_FILE, "r")))

__all__ = ["Config", "config"]
