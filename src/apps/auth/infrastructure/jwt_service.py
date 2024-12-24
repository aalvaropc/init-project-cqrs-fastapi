import jwt
from datetime import datetime, timedelta

class JWTService:
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def generate_token(self, user_id: int, email: str) -> str:
        """
        Genera un token JWT para un usuario.
        """
        payload = {
            "sub": user_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def validate_token(self, token: str) -> dict:
        """
        Valida un token JWT y devuelve su payload.
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
