from django.urls import resolve, reverse


class TestThumbnailsUrls:
    def test_image_detail(self, image):
        assert (
            reverse("image-detail", kwargs={"pk": image.pk})
            == f"/api/v1/images/{image.pk}/"
        )
        assert resolve(f"/api/v1/images/{image.pk}/").view_name == "image-detail"

    def test_image_list(self):
        assert reverse("image-list") == "/api/v1/images/"
        assert resolve("/api/v1/images/").view_name == "image-list"

    def test_expiring_link_detail(self, expiring_link):
        assert (
            reverse("expiring-link-detail", kwargs={"pk": expiring_link.pk})
            == f"/api/v1/expiring-links/{expiring_link.pk}/"
        )
        assert (
            resolve(f"/api/v1/expiring-links/{expiring_link.pk}/").view_name
            == "expiring-link-detail"
        )

    def test_expiring_link_list(self):
        assert reverse("expiring-link-list") == "/api/v1/expiring-links/"
        assert resolve("/api/v1/expiring-links/").view_name == "expiring-link-list"
