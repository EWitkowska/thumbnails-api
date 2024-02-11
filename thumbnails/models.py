from django.db import models
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.conf import settings

from .validators import validate_file_size


def images_directory_path(instance, filename):
    return f"images/{filename}"


class ThumbnailDimension(models.Model):
    width = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], help_text="Enter the width in pixels"
    )
    height = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], help_text="Enter the height in pixels"
    )

    class Meta:
        unique_together = ["width", "height"]

    def __str__(self):
        return f"{self.width}x{self.height}"


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_index=True,
    )
    image = models.ImageField(
        upload_to=images_directory_path,
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"]), validate_file_size],
        help_text="Upload an image file (png, jpg, jpeg), max size 5MB",
    )
    thumbnails = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return f"{self.image.name}"


class ExpiringLink(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_index=True,
    )
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    temporary_link = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_in = models.PositiveIntegerField(
        validators=[MinValueValidator(300), MaxValueValidator(30000)],
        help_text="Select value from 300 to 30000 (seconds) for expiring link to the original image",
    )

    def __str__(self):
        return f"{self.created_at}"
