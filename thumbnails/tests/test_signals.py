import pytest

from thumbnails.models import Image, ExpiringLink


@pytest.mark.django_db
class TestSignals:
    def test_create_thumbnail_signal(self, user, mocker):
        mock_make_thumbnail = mocker.patch("thumbnails.tasks.make_thumbnail.delay")
        image = Image.objects.create(user=user, image="path/to/image.jpg")

        mock_make_thumbnail.assert_called_once_with(image.id)

    def test_create_expiring_link_signal(self, user, image, mocker):
        mock_make_expiring_link = mocker.patch(
            "thumbnails.tasks.make_expiring_link.delay"
        )
        expiring_link = ExpiringLink.objects.create(
            user=user, image=image, expires_in=3600
        )

        mock_make_expiring_link.assert_called_once_with(expiring_link.id)
