post_keywords = [
    "hiring",
    "job opening",
    "looking for developers",
    "developer needed",
    "job opportunity",
]


def check_post(post):
    if any(
        keyword.lower() in post.title.lower()
        or keyword.lower() in post.selftext.lower()
        for keyword in post_keywords
    ):
        return {
            "type": "post",
            "id": post.id,
            "url": f"https://www.reddit.com{post.permalink}",
            "title": post.title,
            "body": post.selftext,
            "author": str(post.author),
            "created_utc": post.created_utc,
        }
    return None
