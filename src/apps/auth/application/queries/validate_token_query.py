from src.apps.auth.infrastructure.jwt_service import JWTService

def validate_token(token: str) -> int:
    """
    Usa la lógica de JWTService para validar el token
    y retornar el user_id. Lanza excepción si es inválido.
    """
    return JWTService.validate_token(token)
