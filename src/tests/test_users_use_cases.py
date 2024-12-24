import pytest
from src.apps.users.domain.use_cases import (
    CreateUserUseCase, GetUserByIdUseCase, 
    UpdateUserUseCase, DeleteUserUseCase
)
from src.apps.users.domain.exceptions import (
    UserAlreadyExistsException, UserNotFoundException
)
from src.apps.users.infrastructure.sqlalchemy_repositories_writer import UserRepositoryWriter

def test_create_user_success(test_db_session):
    repo = UserRepositoryWriter(test_db_session)
    use_case = CreateUserUseCase(repo)

    user = use_case.execute("John", "john@example.com", "1234")
    test_db_session.commit()
    assert user.id is not None

def test_create_user_already_exists(test_db_session):
    repo = UserRepositoryWriter(test_db_session)
    use_case = CreateUserUseCase(repo)
    use_case.execute("John", "john@example.com", "1234")
    test_db_session.commit()

    with pytest.raises(UserAlreadyExistsException):
        use_case.execute("John2", "john@example.com", "abcd")

def test_get_user_not_found(test_db_session):
    repo = UserRepositoryWriter(test_db_session)
    use_case = GetUserByIdUseCase(repo)
    with pytest.raises(UserNotFoundException):
        use_case.execute(999)

def test_update_user_success(test_db_session):
    repo = UserRepositoryWriter(test_db_session)
    create_use_case = CreateUserUseCase(repo)
    created_user = create_use_case.execute("Jane", "jane@example.com", "pwd")
    test_db_session.commit()

    update_use_case = UpdateUserUseCase(repo)
    updated_user = update_use_case.execute(created_user.id, "Jane2", "jane2@example.com")
    test_db_session.commit()

    assert updated_user.name == "Jane2"

def test_delete_user_success(test_db_session):
    repo = UserRepositoryWriter(test_db_session)
    create_use_case = CreateUserUseCase(repo)
    created_user = create_use_case.execute("Mark", "mark@example.com", "pwd")
    test_db_session.commit()

    delete_use_case = DeleteUserUseCase(repo)
    delete_use_case.execute(created_user.id)
    test_db_session.commit()

    # Intentar obtenerlo debe fallar
    get_use_case = GetUserByIdUseCase(repo)
    with pytest.raises(UserNotFoundException):
        get_use_case.execute(created_user.id)
