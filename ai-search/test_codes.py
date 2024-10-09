from dotenv import load_dotenv
from typing import List
from os import getenv
import praw
from datetime import datetime, timedelta
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda

load_dotenv()

reddit = praw.Reddit(
    client_id=getenv("REDDIT_CLIENT_ID"),
    client_secret=getenv("REDDIT_CLIENT_SECRET"),
    user_agent="test",
    username=getenv("REDDIT_ACCOUNT_USERNAME"),
    password=getenv("REDDIT_ACCOUNT_PASSWORD"),
)

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

subreddits = [
    "developersIndia",
]

keywords = ["hiring", "developer", "freelancer", "remote"]
time_threshold = datetime.now() - timedelta(days=1)


def is_job_post(post):
    # Check title or body for keywords
    if any(keyword.lower() in post.title.lower() for keyword in keywords) or any(
        keyword.lower() in post.selftext.lower() for keyword in keywords
    ):
        return True
    return False


def search_job_postings(subreddits: List[str]) -> List:
    results = []
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).new(limit=100):
            post_time = datetime.fromtimestamp(submission.created_utc)

            if post_time > time_threshold and is_job_post(submission):
                # If post matches criteria, store its details
                results.append(
                    {
                        "title": submission.title,
                        "url": submission.url,
                        "subreddit": subreddit,
                        "time": post_time,
                        "summary": submission.selftext[:200],
                    }
                )

    return results


def find_job():
    job_posts = search_job_postings(subreddits)

    if job_posts:
        response = "Job postings found:\n\n"
        for post in job_posts:
            response += f"- [{post['title']}]({post['url']}) in r/{post['subreddit']} at {post['time']} \n\n"
        return response
    else:
        return "No job postings found in the last 24 hours."


if __name__ == "__main__":
    print(find_job())
