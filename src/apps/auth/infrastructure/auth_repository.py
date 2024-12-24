from typing import Optional
from sqlalchemy.orm import Session
from src.apps.auth.domain.repositories import IAuthRepository
from src.apps.users.infrastructure.orm_models import UserModel
import bcrypt

class AuthRepository(IAuthRepository):
    """
    Implementación mínima que reusa la tabla 'users'
    para verificar credenciales.
    """
    def __init__(self, db: Session):
        self.db = db

    def verify_user_credentials(self, email: str, plain_password: str) -> Optional[int]:
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user_model:
            return None

        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), user_model.password_hash.encode('utf-8'))
        if hashed.decode('utf-8') == user_model.password_hash:
            return user_model.id
        return None
    
    def get_user_by_email(self, email: str):
        """
        Recupera un usuario por su correo electrónico.
        """
        return self.db.query(UserModel).filter(UserModel.email == email).first()
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si la contraseña en texto plano coincide con el hash.
        """
        from src.core.hashing import verify_password
        return verify_password(plain_password, hashed_password)