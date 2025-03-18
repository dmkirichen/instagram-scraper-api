from fastapi import FastAPI
from app.scraper import scrape_instagram_posts
from app.celery_tasks import fetch_latest_posts, load_existing_posts


app = FastAPI()

@app.get("/posts")
def get_posts():
    posts = load_existing_posts()
    if posts:
        return {"posts": posts}
    return {"message": "No posts found"}


@app.post("/fetch-latest")
def fetch_latest():
    fetch_latest_posts.delay()
    return {"message": "Fetching is running in the background"}
