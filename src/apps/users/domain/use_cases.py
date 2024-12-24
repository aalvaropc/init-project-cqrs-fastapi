from .repositories import IUserRepository
from .entities import User
from .exceptions import UserAlreadyExistsException, UserNotFoundException

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

class UpdateUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def execute(self, user_id: int, name: str, email: str) -> User:
        user = self._user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        updated_user = self._user_repo.update_user(user_id, name, email)
        return updated_user

class DeleteUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def execute(self, user_id: int) -> None:
        user = self._user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        self._user_repo.delete_user(user_id)

class GetUserByIdUseCase:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    def execute(self, user_id: int) -> User:
        user = self._user_repo.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        return user
