from sqlalchemy.orm import Session
from src.apps.users.infrastructure.orm_models import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def create_user(self, name: str, email: str, password: str):
        user = UserModel(name=name, email=email, password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, name: str = None, email: str = None):
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        if name:
            user.name = name
        if email:
            user.email = email

        self.db.commit()
        self.db.refresh(user)
        return user
