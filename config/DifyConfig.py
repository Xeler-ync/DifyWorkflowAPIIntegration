class DifyConfig:
    def __init__(self, dify_endpoint: str = "", dify_api_key: str = "", user: str = ""):
        self.dify_endpoint = dify_endpoint
        self.dify_api_key = dify_api_key
        self.user = user

    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(
            dify_endpoint=config_dict.get("dify_endpoint", ""),
            dify_api_key=config_dict.get("dify_api_key", ""),
            user=config_dict.get("user", ""),
        )

    def to_dict(self) -> dict:
        return {
            "dify_endpoint": self.dify_endpoint,
            "dify_api_key": self.dify_api_key,
            "user": self.user,
        }

    def __str__(self) -> str:
        return (
            f"DifyConfig("
            f"dify_endpoint='{self.dify_endpoint}', "
            f"dify_api_key='{self.dify_api_key[:8]}...'"
            f"user='{self.user}'"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()
