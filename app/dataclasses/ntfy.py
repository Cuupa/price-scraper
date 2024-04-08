from dataclasses import dataclass

@dataclass
class ntfy:
    url: str
    topic: str
    enabled: bool
    priority: str
    username: str
    password: bytes
    accesstoken: bytes
