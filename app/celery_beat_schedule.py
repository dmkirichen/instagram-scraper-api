from celery.schedules import crontab
from app.celery_config import celery_app
from app.celery_tasks import fetch_latest_posts

celery_app.conf.beat_schedule = {
    "fetch_instagram_posts_every_10_min": {
        "task": "celery_tasks.fetch_latest_posts",
        "schedule": crontab(minute="*/10"),
    }
}
