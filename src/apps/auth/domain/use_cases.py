from src.apps.auth.domain.exceptions import InvalidCredentialsException
from src.apps.auth.domain.repositories import IAuthRepository
from src.apps.auth.domain.exceptions import AuthenticationError
from src.apps.auth.infrastructure.jwt_service import JWTService
from src.apps.auth.infrastructure.auth_repository import AuthRepository
from src.core.config import settings

class LoginUserUseCase:
    def __init__(self, repository: IAuthRepository, jwt_service: JWTService):
        self.repository = repository
        self.jwt_service = jwt_service

    def execute(self, email: str, password: str) -> str:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise AuthenticationError("Usuario no encontrado.")

        if not self.repository.verify_password(password, user.password_hash):
            raise AuthenticationError("Credenciales incorrectas.")

        # Generar el JWT
        return self.jwt_service.generate_token(user.id, user.email)


class ValidateTokenUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, token: str) -> bool:
        return self.repository.validate_token(token)