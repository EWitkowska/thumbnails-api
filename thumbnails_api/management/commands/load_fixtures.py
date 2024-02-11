from django.core.management.base import BaseCommand
from django.core.management import call_command

from users.models import User
from thumbnails.models import ThumbnailDimension


class Command(BaseCommand):
    help = "Load fixtures"

    def handle(self, *args, **options):
        if not ThumbnailDimension.objects.exists():
            call_command("loaddata", "thumbnails/fixtures/thumbnails.yaml")
            self.stdout.write(
                self.style.SUCCESS("Successfully loaded thumbnail fixture")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Thumbnail dimensions already exist, skipping fixture"
                )
            )

        if not User.objects.exists():
            call_command("loaddata", "users/fixtures/users.yaml")
            self.stdout.write(self.style.SUCCESS("Successfully loaded user fixture"))
        else:
            self.stdout.write(
                self.style.SUCCESS("Users already exist, skipping fixture")
            )
