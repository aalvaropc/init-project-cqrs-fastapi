import pytest
from src.apps.users.domain.entities import User

def test_user_hash_password():
    plain_password = "secret"
    hashed = User.hash_password(plain_password)
    assert hashed != plain_password
    assert len(hashed) > 0
