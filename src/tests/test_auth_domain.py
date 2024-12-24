import pytest
from src.apps.users.domain.entities import User

def test_user_hash_and_check_password():
    plain_password = "secret"
    hashed = User.hash_password(plain_password)
    user = User(id=1, name="test", email="test@example.com", password_hash=hashed)

    assert user.check_password("secret") is True
    assert user.check_password("other") is False
