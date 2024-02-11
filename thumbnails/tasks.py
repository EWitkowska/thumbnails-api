import os
from io import BytesIO
from PIL import Image as PILImage
import boto3
from botocore.config import Config
from celery import shared_task
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File

from .models import Image, ExpiringLink


def get_s3_client():
    return boto3.client(
        "s3",
        settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version=settings.AWS_S3_SIGNATURE_VERSION),
    )


@shared_task
def make_thumbnail(pk: str):
    instance = Image.objects.get(id=pk)
    thumbnail_dimensions = instance.user.account_type.thumbnail_dimensions.all()
    links = {}

    format_map = {".jpg": "JPEG", ".png": "PNG"}

    original_image = PILImage.open(instance.image)

    thumb_name, thumb_extension = os.path.splitext(instance.image.name)
    format = format_map.get(thumb_extension, "JPEG")

    for dimension in thumbnail_dimensions:
        width = dimension.width
        height = dimension.height

        thumbnail_image = original_image.copy()
        thumbnail_image.thumbnail((width, height), PILImage.Resampling.LANCZOS)

        file_name = f"{thumb_name}-{width}x{height}{thumb_extension}"

        buffer = BytesIO()
        thumbnail_image.save(buffer, format)
        buffer.seek(0)

        file_object = File(buffer, None)
        file_name = default_storage.save(file_name, file_object)
        url = default_storage.url(file_name)

        links.update({f"thumbnail-{width}x{height}": url})

    instance.thumbnails = links
    instance.save()


@shared_task
def make_expiring_link(pk: str):
    instance = ExpiringLink.objects.get(id=pk)
    client = get_s3_client()

    response = client.generate_presigned_url(
        ClientMethod="get_object",
        ExpiresIn=instance.expires_in,
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": instance.image.image.name,
        },
    )

    instance.temporary_link = response
    instance.save()
