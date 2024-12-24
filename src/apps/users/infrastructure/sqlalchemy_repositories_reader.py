from typing import Optional
from sqlalchemy.orm import Session
from src.apps.users.domain.entities import User
from src.apps.users.domain.repositories import IUserRepository
from src.apps.users.infrastructure.orm_models import UserModel

class UserRepositoryReader(IUserRepository):
    """
    Repositorio para solo lectura. 
    Lanza errores si se intenta escribir.
    """
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, *args, **kwargs):
        raise NotImplementedError("Reader repository does not allow writes.")

    def update_user(self, *args, **kwargs):
        raise NotImplementedError("Reader repository does not allow writes.")

    def delete_user(self, *args, **kwargs):
        raise NotImplementedError("Reader repository does not allow writes.")

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_model:
            return User(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                password_hash=user_model.password_hash
            )
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if user_model:
            return User(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                password_hash=user_model.password_hash
            )
        return None
