import pytest

from unittest.mock import MagicMock, patch
from PIL import Image as PILImage
import tempfile

from thumbnails.tasks import make_thumbnail, make_expiring_link


@pytest.mark.django_db
class TestTasks:
    @patch("thumbnails.tasks.default_storage")
    @patch("thumbnails.tasks.PILImage.open")
    @patch("thumbnails.models.Image.objects.get")
    def test_make_thumbnail(self, mock_get, mock_open, mock_storage):
        mock_image = MagicMock()
        mock_get.return_value = mock_image

        img = PILImage.new("RGB", (100, 100), color="red")
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            img.save(temp_file.name)
            mock_image.image.file.name = temp_file.name

        mock_dimension = MagicMock()
        mock_dimension.width = 100
        mock_dimension.height = 100
        mock_image.user.account_type.thumbnail_dimensions.all.return_value = [
            mock_dimension
        ]

        mock_img = MagicMock()
        mock_open.return_value = mock_img

        mock_storage.save.return_value = "test_filename"
        mock_storage.url.return_value = "test_url"

        make_thumbnail("test_pk")

        mock_get.assert_called_once_with(id="test_pk")
        mock_storage.save.assert_called()
        mock_storage.url.assert_called()
        assert mock_image.thumbnails
        mock_image.save.assert_called_once()

    @patch("thumbnails.tasks.get_s3_client")
    @patch("thumbnails.models.ExpiringLink.objects.get")
    def test_make_expiring_link(self, mock_get, mock_s3_client):
        mock_link = MagicMock()
        mock_get.return_value = mock_link

        mock_client = MagicMock()
        mock_s3_client.return_value = mock_client

        mock_client.generate_presigned_url.return_value = "test_url"

        make_expiring_link("test_pk")

        mock_get.assert_called_once_with(id="test_pk")
        mock_client.generate_presigned_url.assert_called()
        assert mock_link.temporary_link == "test_url"
        mock_link.save.assert_called_once()
