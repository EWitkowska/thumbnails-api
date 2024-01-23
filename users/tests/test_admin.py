import pytest

from django.urls import reverse
from django.test import Client

from users.models import User, Account


class TestUserAdmin:
    @pytest.fixture
    def admin_client(self):
        client = Client()
        admin_user = User.objects.create_superuser("admin@example.com", "password123")
        client.force_login(admin_user)

        return client

    @pytest.mark.django_db
    def test_changelist(self, admin_client: admin_client):
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url)

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_search(self, admin_client: admin_client):
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url, data={"q": "test"})

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_add(self, admin_client: admin_client):
        url = reverse("admin:users_user_add")
        response = admin_client.get(url)

        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                "email": "new-admin@example.com",
                "password1": "My_R@ndom-P@ssw0rd",
                "password2": "My_R@ndom-P@ssw0rd",
            },
        )

        assert response.status_code == 302
        assert User.objects.filter(email="new-admin@example.com").exists()

    @pytest.mark.django_db
    def test_view_user(self, admin_client: admin_client):
        user = User.objects.create_user("test@example.com", "password123")
        url = reverse("admin:users_user_change", kwargs={"object_id": user.pk})
        response = admin_client.get(url)

        assert response.status_code == 200


class TestAccountAdmin:
    @pytest.fixture
    def admin_client(self):
        client = Client()
        admin_user = User.objects.create_superuser("admin@example.com", "password123")
        client.force_login(admin_user)

        return client

    @pytest.mark.django_db
    def test_changelist(self, admin_client):
        url = reverse("admin:users_account_changelist")
        response = admin_client.get(url)

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_search(self, admin_client):
        url = reverse("admin:users_account_changelist")
        response = admin_client.get(url, data={"q": "test"})

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_add(self, admin_client):
        url = reverse("admin:users_account_add")
        response = admin_client.get(url)

        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                "name": "New Account",
                "can_retrieve_original_image": True,
                "can_generate_expiring_link": True,
            },
        )

        assert response.status_code == 302
        assert Account.objects.filter(name="New Account").exists()

    @pytest.mark.django_db
    def test_view_account(self, admin_client):
        account = Account.objects.create(name="Test Account")
        url = reverse("admin:users_account_change", kwargs={"object_id": account.pk})
        response = admin_client.get(url)

        assert response.status_code == 200
