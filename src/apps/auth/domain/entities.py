from dataclasses import dataclass

@dataclass
class AuthSession:
    token: str
    user_id: int
