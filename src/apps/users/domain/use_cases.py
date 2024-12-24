from .repositories import IUserRepository
from .entities import User
from .exceptions import UserAlreadyExistsException, UserNotFoundException
from sqlalchemy.orm import Session
from src.apps.users.infrastructure.orm_models import UserModel
class CreateUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def execute(self, name: str, email: str, password: str) -> User:
        existing_user = self._user_repo.get_user_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExistsException(email)

        password_hash = User.hash_password(password)
        new_user = self._user_repo.create_user(name, email, password_hash)
        return new_user

class DeleteUserUseCase:
    def __init__(self, repo: IUserRepository):
        self._repo = repo

    def execute(self, user_id: int):
        user = self._repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        self._repo.delete_user(user_id)

class GetUserByIdUseCase:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def execute(self, user_id: int) -> User:
        user = self._user_repo.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        return user

class UpdateUserUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, user_id: int, name: str = None, email: str = None):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise UserNotFoundException("User not found.")

        if email and self.db.query(UserModel).filter(UserModel.email == email).first():
            raise ValueError("Email already exists.")

        if name:
            user.name = name
        if email:
            user.email = email

        self.db.commit()
        self.db.refresh(user)
        return user