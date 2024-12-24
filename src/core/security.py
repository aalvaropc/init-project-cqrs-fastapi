import jwt
import datetime
from src.core.config import settings

def create_jwt_token(user_id: int) -> str:
    """
    Genera un token JWT con fecha de expiración.
    """
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

def verify_jwt_token(token: str) -> int:
    """
    Decodifica el token JWT y retorna el user_id contenido en "sub".
    Lanza excepción si el token es inválido o está expirado.
    """
    decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    return int(decoded["sub"])
