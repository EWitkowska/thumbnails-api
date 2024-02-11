import pytest

from unittest import mock
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.views import APIView

from users.models import User
from thumbnails.models import ThumbnailDimension, Image, ExpiringLink
from thumbnails.permissions import CanGenerateImages

CELERY_BROKER_URL = "memory://"


@pytest.fixture
def admin_client(db):
    client = Client()
    admin_user = User.objects.create_superuser("admin@example.com", "password123")
    client.force_login(admin_user)
    return client


@pytest.fixture
def user(db):
    return User.objects.create(
        email="test@example.com", password="testpassword", account_type=None
    )


@pytest.fixture
def thumbnail_dimension(db):
    return ThumbnailDimension.objects.create(width=200, height=200)


@pytest.fixture
def image(user):
    image_file = SimpleUploadedFile(
        name="test_image.jpg", content=b"", content_type="image/jpeg"
    )
    return Image.objects.create(user=user, image=image_file)


@pytest.fixture
def expiring_link(user, image):
    return ExpiringLink.objects.create(
        user=user, image=image, temporary_link="http://temp.link", expires_in=300
    )


@pytest.fixture(autouse=True)
def mock_redis_connection(mocker):
    with mock.patch("redis.Redis", autospec=True):
        with mock.patch("celery.app.base.Celery.send_task"):
            yield


@pytest.fixture
def view():
    return APIView()


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.fixture
def api_client():
    return APIClient()
