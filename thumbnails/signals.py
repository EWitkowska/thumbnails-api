from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Image, ExpiringLink
from .tasks import make_thumbnail, make_expiring_link


@receiver(post_save, sender=Image)
def create_thumbnail(sender, instance, created, **kwargs):
    if created:
        make_thumbnail.delay(instance.id)


@receiver(post_save, sender=ExpiringLink)
def create_expiring_link(sender, instance, created, **kwargs):
    if created:
        make_expiring_link.delay(instance.id)
