from celery import Celery
import os

CELERY_BROKER = os.getenv("CELERY_BROKER", "redis://redis:6379/0")
CELERY_BACKEND = os.getenv("CELERY_BACKEND", "redis://redis:6379/0")

celery_app = Celery("tasks", broker=CELERY_BROKER, backend=CELERY_BACKEND)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    beat_schedule={},
)
