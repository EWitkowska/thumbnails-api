import pytest

from thumbnails.permissions import CanGenerateExpiringLink, CanGenerateImages
from users.models import Account


class TestCanGenerateImages:
    @pytest.fixture
    def permission(self):
        return CanGenerateImages()

    def test_has_permission_unauthenticated(self, permission, view, request_factory):
        request = request_factory.get("/")
        request.user = None
        assert permission.has_permission(request, view) == False

    def test_has_permission_no_account_type(
        self, permission, view, request_factory, user
    ):
        request = request_factory.get("/")
        request.user = user
        assert permission.has_permission(request, view) == False

    def test_has_permission_with_account_type(
        self,
        permission,
        view,
        request_factory,
        user,
    ):
        account = Account.objects.create(name="Basic")
        user.account_type = account
        request = request_factory.get("/")
        request.user = user
        assert permission.has_permission(request, view) == True


class TestCanGenerateExpiringLink:
    @pytest.fixture
    def permission(self):
        return CanGenerateExpiringLink()

    def test_has_permission_unauthenticated(self, permission, view, request_factory):
        request = request_factory.get("/")
        request.user = None
        assert permission.has_permission(request, view) == False

    def test_has_permission_no_account_type(
        self, permission, view, request_factory, user
    ):
        request = request_factory.get("/")
        request.user = user
        assert permission.has_permission(request, view) == False

    def test_has_permission_cannot_generate_link(
        self,
        permission,
        view,
        request_factory,
        user,
    ):
        account = Account.objects.create(name="Basic")
        account.can_generate_expiring_link = False
        user.account_type = account
        request = request_factory.get("/")
        request.user = user
        assert permission.has_permission(request, view) == False

    def test_has_permission_can_generate_link(
        self,
        permission,
        view,
        request_factory,
        user,
    ):
        account = Account.objects.create(name="Enterprise")
        account.can_generate_expiring_link = True
        user.account_type = account
        request = request_factory.get("/")
        request.user = user
        assert permission.has_permission(request, view) == True
