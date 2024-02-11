import pytest

from PIL import Image as PILImage
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

from thumbnails.models import Image
from thumbnails.serializers import ImageSerializer, ExpiringLinkSerializer
from users.models import Account


@pytest.mark.django_db
class TestImageSerializer:
    def test_create(self, user, request_factory):
        image_io = BytesIO()
        image = PILImage.new("RGB", (100, 100))
        image.save(image_io, format="JPEG")
        image_io.seek(0)
        image_file = SimpleUploadedFile(
            "test.jpg", image_io.read(), content_type="image/jpeg"
        )

        request = request_factory.get("/")
        request.user = user
        serializer = ImageSerializer(
            data={"user": user, "image": image_file, "thumbnails": None},
            context={"request": request},
        )

        assert serializer.is_valid()
        image = serializer.save()
        assert image.user == user

    def test_to_representation_without_permission(self, user):
        account = Account.objects.create(name="Basic")
        account.can_retrieve_original_image = False
        user.account_type = account
        image = Image.objects.create(user=user, image="path/to/image.jpg")

        serializer = ImageSerializer(image)
        representation = serializer.data

        assert (
            representation["image"]
            == "You don't have permission to retrieve this image."
        )

    def test_to_representation_with_permission(self, user):
        account = Account.objects.create(name="Premium")
        account.can_retrieve_original_image = True
        user.account_type = account
        image = Image.objects.create(user=user, image="path/to/image.jpg")

        serializer = ImageSerializer(image)
        representation = serializer.data
        full_url = image.image.url

        assert representation["image"] == full_url


@pytest.mark.django_db
class TestExpiringLinkSerializer:
    def test_init(self, user, request_factory):
        request = request_factory.get("/")
        request.user = user

        serializer = ExpiringLinkSerializer(context={"request": request})

        assert (
            serializer.fields["image"].queryset.first()
            == Image.objects.filter(user=request.user).first()
        )

    def test_create(self, user, request_factory):
        account = Account.objects.create(name="Premium")
        account.can_generate_expiring_link = True
        user.account_type = account
        image = Image.objects.create(user=user, image="path/to/image.jpg")

        request = request_factory.get("/")
        request.user = user
        serializer = ExpiringLinkSerializer(
            data={"image": image.id, "expires_in": 3600}, context={"request": request}
        )

        assert serializer.is_valid()
        expiring_link = serializer.save()
        assert expiring_link.user == user
