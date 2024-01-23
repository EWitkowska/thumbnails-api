import pytest

from django.test import Client
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def user(db):
    return User.objects.create(email="test@example.com", password="testpassword")


@pytest.fixture
def admin_client():
    client = Client()
    admin_user = User.objects.create_superuser("admin@example.com", "password123")
    client.force_login(admin_user)

    return client


@pytest.fixture
def api_client():
    return APIClient()
