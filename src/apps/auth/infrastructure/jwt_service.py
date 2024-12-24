from src.core.security import create_jwt_token, verify_jwt_token

class JWTService:
    @staticmethod
    def generate_token(user_id: int) -> str:
        return create_jwt_token(user_id)

    @staticmethod
    def validate_token(token: str) -> int:
        return verify_jwt_token(token)
