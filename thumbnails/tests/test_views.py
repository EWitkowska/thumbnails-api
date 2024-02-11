from thumbnails.views import ImageViewSet, ExpiringLinkViewSet
from thumbnails.serializers import (
    ListImageSerializer,
    ImageSerializer,
    ListExpiringLinkSerializer,
    ExpiringLinkSerializer,
)


class TestImageViewSet:
    def test_get_serializer_class(self, user, api_client):
        view = ImageViewSet()
        request = api_client.get(f"/api/v1/images/")
        request.user = user

        view.request = request
        view.action = "list"

        assert view.get_serializer_class() is ListImageSerializer

        view.action = "retrieve"

        assert view.get_serializer_class() is ImageSerializer

    def test_get_queryset(self, user, image, api_client):
        view = ImageViewSet()
        request = api_client.get(f"/api/v1/images/")
        request.user = user

        view.request = request

        assert image in view.get_queryset()


class TestExpiringLinkViewSet:
    def test_get_serializer_class(self, user, api_client):
        view = ExpiringLinkViewSet()
        request = api_client.get(f"/api/v1/expiring-links/")
        request.user = user

        view.request = request
        view.action = "list"

        assert view.get_serializer_class() is ListExpiringLinkSerializer

        view.action = "retrieve"

        assert view.get_serializer_class() is ExpiringLinkSerializer

    def test_get_queryset(self, user, expiring_link, api_client):
        view = ExpiringLinkViewSet()
        request = api_client.get(f"/api/v1/expiring-links/")
        request.user = user

        view.request = request

        assert expiring_link in view.get_queryset()
