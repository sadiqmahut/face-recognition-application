import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "face_attendace.settings")
app = Celery("face_attendace")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()