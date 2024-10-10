comment_keywords = [
    "job opening",
    "hiring",
    "job opportunity",
    "looking for candidates",
]


def check_comment(comment):
    if any(keyword.lower() in comment.body.lower() for keyword in comment_keywords):
        return {
            "type": "comment",
            "id": comment.id,
            "url": f"https://www.reddit.com{comment.permalink}",
            "body": comment.body,
            "author": str(comment.author),
            "created_utc": comment.created_utc,
        }
    return None
