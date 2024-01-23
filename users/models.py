from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField

from .managers import UserManager
from thumbnails.models import ThumbnailDimension


class User(AbstractUser):
    first_name = None
    last_name = None
    email = EmailField("email address", unique=True)
    username = None
    account_type = models.ForeignKey(
        "users.Account",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email


class Account(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Account type name (e.g. 'Basic', 'Premium')",
    )
    thumbnail_dimensions = models.ManyToManyField(
        ThumbnailDimension, blank=True, related_name="accounts"
    )
    can_retrieve_original_image = models.BooleanField(default=False)
    can_generate_expiring_link = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
