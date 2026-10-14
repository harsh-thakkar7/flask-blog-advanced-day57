from flask import Flask, render_template
from post import Post
import requests

API_URL = "https://api.npoint.io/5abcca6f4e39b4955965"
FALLBACK_POSTS = [
    {
        "id": 1,
        "title": "The Life of Cactus",
        "subtitle": "How to care for a prickly friend.",
        "body": "Cacti are resilient plants that thrive in warm, dry conditions. They need plenty of sunlight, minimal watering, and well-draining soil to stay healthy. With the right care, a cactus can become a long-lasting, low-maintenance companion.",
    },
    {
        "id": 2,
        "title": "Sunrise Walks",
        "subtitle": "A peaceful way to start the day.",
        "body": "Morning walks are a simple ritual that can improve both mood and energy. The fresh air, calm surroundings, and quiet rhythm of the day help clear the mind and make room for clearer thinking.",
    },
    {
        "id": 3,
        "title": "The Power of Small Habits",
        "subtitle": "Tiny routines that create big change.",
        "body": "Consistency matters more than intensity. When you build small, sustainable habits, they compound over time and slowly transform your life in ways that feel natural and lasting.",
    },
]

app = Flask(__name__)


def load_posts():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        payload = response.json()
        if isinstance(payload, list):
            return payload
    except (requests.RequestException, ValueError):
        pass
    return FALLBACK_POSTS


posts = [post for post in load_posts() if isinstance(post, dict)]
post_objects = [
    Post(post.get("id", idx + 1), post.get("title", "Untitled"), post.get("subtitle", ""), post.get("body", ""))
    for idx, post in enumerate(posts)
]


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=post_objects)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = next((blog_post for blog_post in post_objects if blog_post.id == index), None)
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001)


