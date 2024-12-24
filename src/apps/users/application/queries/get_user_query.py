from sqlalchemy.orm import Session
from src.apps.users.domain.use_cases import GetUserByIdUseCase
from src.apps.users.infrastructure.sqlalchemy_repositories_reader import UserRepositoryReader

def get_user_by_id(db: Session, user_id: int):
    repo = UserRepositoryReader(db)
    use_case = GetUserByIdUseCase(repo)
    return use_case.execute(user_id)
