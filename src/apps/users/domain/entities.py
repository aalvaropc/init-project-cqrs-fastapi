from dataclasses import dataclass
import bcrypt

@dataclass
class User:
    id: int
    name: str
    email: str
    password_hash: str

    @staticmethod
    def hash_password(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, plain_password: str) -> bool:
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), self.password_hash.encode('utf-8'))
        return hashed.decode('utf-8') == self.password_hash
