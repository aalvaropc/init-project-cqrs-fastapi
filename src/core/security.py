import jwt
import datetime
from src.core.config import settings
from fastapi import Header, HTTPException
from src.apps.auth.infrastructure.jwt_service import JWTService

# def create_jwt_token(user_id: int) -> str:
#     """
#     Genera un token JWT con fecha de expiración.
#     """
#     expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
#     payload = {
#         "sub": str(user_id),
#         "exp": expire
#     }
#     token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
#     return token

# def verify_jwt_token(token: str) -> int:
#     """
#     Decodifica el token JWT y retorna el user_id contenido en "sub".
#     Lanza excepción si el token es inválido o está expirado.
#     """
#     decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
#     return int(decoded["sub"])


def get_current_user(token: str = Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    jwt_service = JWTService(
        secret_key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
        expire_minutes=settings.JWT_EXPIRE_MINUTES
    )

    try:
        payload = jwt_service.validate_token(token)
        return payload.get("sub")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))