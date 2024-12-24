from src.apps.auth.domain.exceptions import InvalidCredentialsException
from src.apps.auth.domain.repositories import IAuthRepository
from src.apps.auth.domain.exceptions import AuthenticationError
from src.apps.auth.infrastructure.jwt_service import JWTService
from src.apps.auth.infrastructure.auth_repository import AuthRepository

class LoginUserUseCase:
    def __init__(self, repository: AuthRepository, jwt_service: JWTService):
        self.repository = repository
        self.jwt_service = jwt_service

    def execute(self, email: str, password: str) -> str:
        """
        Valida las credenciales del usuario y genera un JWT.

        :param email: Email del usuario.
        :param password: Contraseña del usuario.
        :return: JWT generado.
        """
        user = self.repository.get_user_by_email(email)
        if not user:
            raise AuthenticationError("Usuario no encontrado.")

        if not self.repository.verify_password(password, user.password_hash):
            raise AuthenticationError("Contraseña incorrecta.")

        token_data = {
            "sub": str(user.id),
            "email": user.email
        }
        access_token = self.jwt_service.create_jwt_token(user_id=user.id)
        return access_token

class ValidateTokenUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, token: str) -> bool:
        # Lógica para validar el token
        return self.repository.validate_token(token)