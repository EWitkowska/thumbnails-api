import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from thumbnails.models import ThumbnailDimension, Image, ExpiringLink


def test_images_directory_path(user, mocker):
    mock_save = mocker.patch("thumbnails.models.Image.save", return_value=None)
    image_file = SimpleUploadedFile(
        name="test_image.jpg", content=b"", content_type="image/jpeg"
    )
    image = Image.objects.create(user=user, image=image_file)

    assert image.image.name == "test_image.jpg"
    mock_save.assert_called_once()


class TestThumbnailDimension:
    def test_str(self):
        dimension = ThumbnailDimension(width=200, height=200)
        assert str(dimension) == "200x200"

    def test_width_validation(self):
        with pytest.raises(ValidationError):
            ThumbnailDimension(width=0, height=200).full_clean()

    def test_height_validation(self):
        with pytest.raises(ValidationError):
            ThumbnailDimension(width=200, height=0).full_clean()


class TestImage:
    @pytest.mark.django_db
    def test_user_cannot_be_null(self, mocker):
        mocker.patch(
            "django.core.files.storage.default_storage.save",
            return_value="path/to/image.jpg",
        )
        mocker.patch("thumbnails.tasks.make_thumbnail.delay")
        image_file = SimpleUploadedFile(
            name="test_image.jpg", content=b"", content_type="image/jpeg"
        )
        with pytest.raises(IntegrityError):
            image = Image.objects.create(user=None, image=image_file)

    def test_image_field_validation(self, user, mocker):
        mocker.patch(
            "django.core.files.storage.default_storage.save",
            return_value="path/to/image.gif",
        )
        mocker.patch("thumbnails.tasks.make_thumbnail.delay")
        image = Image(user=user, image="invalid_image_file.gif")
        with pytest.raises(ValidationError):
            image.full_clean()

    def test_thumbnails_can_be_null(self, user, mocker):
        mocker.patch(
            "django.core.files.storage.default_storage.save",
            return_value="path/to/image.jpg",
        )
        mocker.patch("thumbnails.tasks.make_thumbnail.delay")
        image_file = SimpleUploadedFile(
            name="test_image.jpg", content=b"", content_type="image/jpeg"
        )
        image = Image.objects.create(user=user, image=image_file, thumbnails=None)
        image.full_clean()


class TestExpiringLink:
    @pytest.mark.django_db
    def test_expires_in_validator(self, user, mocker):
        mocker.patch(
            "django.core.files.storage.default_storage.save",
            return_value="path/to/image.jpg",
        )
        mocker.patch("thumbnails.tasks.make_thumbnail.delay")
        image_file = SimpleUploadedFile(
            name="test_image.jpg", content=b"", content_type="image/jpeg"
        )

        image = Image.objects.create(user=user, image=image_file)

        link = ExpiringLink(user=user, image=image, expires_in=299)
        with pytest.raises(ValidationError):
            link.full_clean()

        link = ExpiringLink(user=user, image=image, expires_in=30001)
        with pytest.raises(ValidationError):
            link.full_clean()

        link = ExpiringLink(user=user, image=image, expires_in=15000)
        try:
            link.full_clean()
        except ValidationError:
            pytest.fail("full_clean() raised ValidationError unexpectedly!")
