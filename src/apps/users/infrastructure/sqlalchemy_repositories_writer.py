from typing import Optional
from sqlalchemy.orm import Session
from src.apps.users.domain.entities import User
from src.apps.users.domain.repositories import IUserRepository
from src.apps.users.infrastructure.orm_models import UserModel

class UserRepositoryWriter(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, name: str, email: str, password_hash: str) -> User:
        user_model = UserModel(name=name, email=email, password_hash=password_hash)
        self.db.add(user_model)
        self.db.flush()
        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password_hash=user_model.password_hash
        )

    def update_user(self, user_id: int, name: str = None, email: str = None):
        """
        Update a user's information.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found.")

        if name:
            user.name = name
        if email:
            user.email = email

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        """
        Deletes a user by their ID.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        self.db.delete(user)
        self.db.commit()

    def get_user_by_id(self, user_id: int):
        """
        Fetch a user by their ID.
        """
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()                                                                                                                                                                                                                                                                              

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
