import pytest

from django.urls import reverse

from thumbnails.models import ThumbnailDimension


class TestThumbnailDimensionAdmin:
    @pytest.mark.django_db
    def test_add(self, admin_client):
        url = reverse("admin:thumbnails_thumbnaildimension_add")
        response = admin_client.get(url)
        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                "width": 300,
                "height": 300,
            },
        )

        assert response.status_code == 302
        assert ThumbnailDimension.objects.filter(width=300, height=300).exists()

    @pytest.mark.django_db
    def test_changelist(self, admin_client):
        url = reverse("admin:thumbnails_thumbnaildimension_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_search(self, admin_client):
        url = reverse("admin:thumbnails_thumbnaildimension_changelist")
        response = admin_client.get(url, data={"q": "200x200"})
        assert response.status_code == 200


class TestImageAdmin:
    @pytest.mark.django_db
    def test_changelist(self, admin_client):
        url = reverse("admin:thumbnails_image_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_search(self, admin_client):
        url = reverse("admin:thumbnails_image_changelist")
        response = admin_client.get(url, data={"q": "admin@example.com"})
        assert response.status_code == 200


class TestExpiringLinkAdmin:
    @pytest.mark.django_db
    def test_changelist(self, admin_client):
        url = reverse("admin:thumbnails_expiringlink_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_search(self, admin_client):
        url = reverse("admin:thumbnails_expiringlink_changelist")
        response = admin_client.get(url, data={"q": "http://temp.link"})
        assert response.status_code == 200
