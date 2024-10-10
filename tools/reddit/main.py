from datetime import datetime, timedelta
import json
from os import getenv
import concurrent
import time
from dotenv import load_dotenv
from praw import Reddit
from reddit_comments import check_comment
from reddit_posts import check_post

load_dotenv()

reddit = Reddit(
    client_id=getenv("REDDIT_CLIENT_ID"),
    client_secret=getenv("REDDIT_CLIENT_SECRET"),
    user_agent="test",
    username=getenv("REDDIT_ACCOUNT_USERNAME"),
    password=getenv("REDDIT_ACCOUNT_PASSWORD"),
)

subreddits = [
    "cscareerquestions",
    "forhire",
    "jobbit",
    "remotejs",
    "devopsjobs",
    "developersIndia",
]


def scrape_subreddit(subreddit_name, end_time):
    subreddit = reddit.subreddit(subreddit_name)
    results = []
    end_time = datetime.now() + end_time

    while datetime.now() < end_time:
        try:
            for submission in subreddit.new(limit=10):
                submission_time = datetime.fromtimestamp(submission.created_utc)
                if submission_time < (datetime.now() - timedelta(minutes=60)):
                    break

                post_result = check_post(submission)
                if post_result:
                    print(f"POST FOUND IN SUBREDDIT r/{subreddit_name} \n")
                    print(post_result)
                    print("_________________________________________________\n")
                    results.append(post_result)
                else:
                    submission.comments.replace_more(limit=10)
                    for comment in submission.comments.list():
                        comment_result = check_comment(comment)
                        if comment_result:
                            print(
                                f"COMMENT FOUND IN SUBREDDIT r/{subreddit_name} under post {submission.title[:10]}...\n"
                            )
                            print(comment_result)
                            print("_________________________________________________\n")
                            results.append(comment_result)

            print(f"Scraped subreddit r/{subreddit_name} \n")
            print("__________________________________________________________\n")
            return results
            # time.sleep(30)  # Wait before checking again
        except Exception as e:
            print(f"An error occurred in r/{subreddit_name}: {e}")
            time.sleep(60)  # Wait before retrying

    # return results


def scrape_reddit_jobs(restart_interval_minutes=60, max_workers=10, batch_size=10):
    print(
        f"Starting to monitor {len(subreddits)} subreddits for job-related posts and comments..."
    )

    while True:
        cycle_start_time = datetime.now()
        all_results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(0, len(subreddits), batch_size):
                batch = subreddits[i : i + batch_size]

                future_to_subreddit = {
                    executor.submit(
                        scrape_subreddit,
                        subreddit,
                        timedelta(minutes=5),
                    ): subreddit
                    for subreddit in batch
                }
                for future in concurrent.futures.as_completed(future_to_subreddit):
                    subreddit = future_to_subreddit[future]
                    try:
                        results = future.result()
                        all_results.extend(results)
                        print(f"Finished scraping r/{subreddit}")
                    except Exception as e:
                        print(f"r/{subreddit} generated an exception: {e}")

        process_results(all_results)

        elapsed_time = datetime.now() - cycle_start_time
        wait_time = max(
            timedelta(0), timedelta(minutes=restart_interval_minutes) - elapsed_time
        )
        print(
            f"Finished processing all subreddits. Waiting {wait_time.total_seconds():.2f} seconds before restarting."
        )
        break
        # time.sleep(wait_time.total_seconds())


def process_results(results):
    print(f"Processing {len(results)} results...")
    print(json.dumps(results))


def get_reddit_jobs():
    scrape_reddit_jobs(restart_interval_minutes=60, max_workers=10, batch_size=10)


if __name__ == "__main__":
    get_reddit_jobs()
