import os
import requests
from fastapi import FastAPI
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
USER_ID = os.getenv("INSTAGRAM_USER_ID")
HASHTAGS = os.getenv("FILTER_HASHTAGS").split(",")
BASE_URL = "https://graph.instagram.com"

app = FastAPI()

celery = Celery("tasks", broker=os.getenv("CELERY_BROKER_URL"), backend=os.getenv("CELERY_BACKEND_URL"))


def get_instagram_posts():
    url = f"{BASE_URL}/{USER_ID}/media?fields=id,caption,permalink&access_token={ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        posts = response.json().get("data", [])[:10]
        return [{"id": post["id"], "caption": post.get("caption", ""), "url": post["permalink"]} for post in posts]
    return {"error": "Failed to fetch posts"}


@app.get("/posts")
def fetch_posts():
    return get_instagram_posts()

@app.get("/check-hashtags")
def check_hashtags():
    posts = get_instagram_posts()
    if posts.get("error"):
        return posts
    
    filtered_posts = [p for p in posts if any(h in p["caption"] for h in HASHTAGS)]
    return {"posts": filtered_posts}

@app.get("/update-posts")
def trigger_update():
    celery.send_task("tasks.update_posts")
    return {"message": "Update started"}
