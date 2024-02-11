from django.apps import AppConfig


class ThumbnailsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "thumbnails"

    def ready(self):
        import thumbnails.signals
