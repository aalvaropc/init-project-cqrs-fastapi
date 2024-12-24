from abc import ABC, abstractmethod
from typing import Optional
from .entities import User

class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, name: str, email: str, password_hash: str) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id: int, name: str, email: str) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass
