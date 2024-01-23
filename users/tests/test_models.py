import pytest

from users.models import User, Account


class TestAccountModel:
    @pytest.mark.django_db
    def test_create_account(self):
        account = Account.objects.create(name="Basic")

        assert account.name == "Basic"

    @pytest.mark.django_db
    def test_account_str(self):
        account = Account.objects.create(name="Basic")

        assert str(account) == "Basic"


class TestUserAccount:
    @pytest.mark.django_db
    def test_user_account_relationship(self):
        account = Account.objects.create(name="Basic")
        user = User.objects.create(email="test@example.com", account_type=account)

        assert user.account_type == account
