import pytest

from users.models import User


@pytest.fixture
def user(db):
    return User.objects.create(email="test@example.com", password="testpassword")
