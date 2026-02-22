import os

import dotenv
from celery import Celery
from pathlib import Path


dotenv.read_dotenv(Path(__file__).resolve().parent.parent / ".env")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("lottery")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
