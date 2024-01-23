import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thumbnails_api.settings")

app = Celery("thumbnails_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
