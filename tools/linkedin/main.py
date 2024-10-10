from os import getenv
from linkedin_api import Linkedin
from dotenv import load_dotenv

load_dotenv()

api = Linkedin(
    username=getenv("LINKEDIN_ACCOUNT_USERNAME"),
    password=getenv("LINKEDIN_ACCOUNT_PASSWORD"),
)

results = api.search_jobs(keywords="Web Developer")

print(results)
