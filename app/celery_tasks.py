from app.celery_config import celery_app
from app.scraper import scrape_instagram_posts, DATA_FILE
import json
import os


def load_existing_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


@celery_app.task
def fetch_latest_posts():
    return scrape_instagram_posts()
