import json

def load_posted_links(path="posted_news.json"):
    try:
        with open(path, "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_posted_links(posted_links, path="posted_news.json"):
    with open(path, "w") as f:
        json.dump(list(posted_links), f)
