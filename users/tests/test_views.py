import pytest

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from users.views import UserViewSet


class TestUserViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    def test_get_queryset(self, user, api_client: APIClient):
        view = UserViewSet()
        request = api_client.get(f"/api/v1/users/{user.pk}")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_partial_update_success(self, user, api_client: APIClient):
        api_client.force_authenticate(user)
        response = api_client.put(
            f"/api/v1/users/{user.pk}/", {"email": "new@example.com"}
        )
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.email == "new@example.com"

    def test_partial_update_invalid_field(self, user, api_client: APIClient):
        api_client.force_authenticate(user)
        response = api_client.put(f"/api/v1/users/{user.pk}/", {"url": "/fake-url/"})
        user.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "email": [ErrorDetail(string="This field is required.", code="required")],
        }
