import json
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

INSTAGRAM_URL = "https://www.instagram.com/nasa/"
HASHTAGS = os.getenv("FILTER_HASHTAGS").split(",")
DATA_FILE = os.getenv("DATA_FILE", "posts.json")


def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)


def parse_int(s):
    if s[-1] == "K":
        return int(s[:-1]) * 1000
    elif s[-1] == "M":
        return int(s[:-1]) * 1000000
    elif s[-1] == "B":
        return int(s[:-1]) * 1000000000
    else:
        return int(s)


def parse_likes_comments(description):
    parts = description.split(" ")
    try:
        likes = parse_int(parts[0].replace(",", ""))
        comments = parse_int(parts[2].replace(",", ""))
        return likes, comments
    except (IndexError, ValueError):
        return 0, 0

 
def scrape_instagram_posts():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # no need for gui
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium"

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
    driver.get(INSTAGRAM_URL)
    time.sleep(5)  # wait for the page to load

    posts_data = []
    post_links = []
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        post_url = link.get_attribute("href")
        if "/p/" in post_url:
            post_links.append(post_url)
        if len(post_links) >= 10:
            break

    print(f"post_links = {post_links}")
    for post_link in post_links:
        driver.get(post_link)
        time.sleep(3)

        try:
            description = driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute("content")
            likes, comments = parse_likes_comments(description.strip())
            has_hashtag = any((f'#{h}' in description for h in HASHTAGS))

            posts_data.append({
                "link": post_link,
                "description": description,
                "likes": likes,
                "comments": comments,
                "has_hashtag": has_hashtag
            })
        except Exception as e:
            print(f"Parsing error for {post_link}: {e}")

    driver.quit()

    print(f"posts_data = {posts_data}")
    save_posts(posts_data)

    return posts_data


if __name__ == "__main__":
    print(scrape_instagram_posts())
