import logging
from typing import Optional
from .DifyConfig import DifyConfig


class Config:
    def __init__(
        self,
        address: str = "0.0.0.0",
        port: int = 54798,
        log_level: str = "WARNING",
        dify: Optional[DifyConfig] = None,
    ):
        self.address = address
        self.port = port
        self.log_level = getattr(logging, log_level, logging.INFO)
        self.dify = dify or DifyConfig()

    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(
            address=config_dict.get("address", "0.0.0.0"),
            port=config_dict.get("port", 54798),
            log_level=config_dict.get("log_level", "WARNING"),
            dify=DifyConfig.from_dict(config_dict.get("dify", {})),
        )

    def to_dict(self) -> dict:
        return {
            "address": self.address,
            "port": self.port,
            "log_level": self.log_level,
            "dify": self.dify.to_dict(),
        }

    def __str__(self) -> str:
        return (
            f"Config("
            f"address='{self.address}', "
            f"port={self.port}, "
            f"log_level='{logging.getLevelName(self.log_level)}', "
            f"dify={self.dify}"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()
