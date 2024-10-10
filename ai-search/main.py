from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from model.gemini import gemini_model

load_dotenv()


def scrape_reddit_jobs():

    return ["Looking for a Python developer", "Seeking a React developer"]


def scrape_linkedin_jobs():
    return ["Hiring a Full-Stack developer", "We need a Data Scientist"]


def analyze_reddit_posts(posts):
    return posts


def analyze_linkedin_posts(posts):
    return posts


def combine_reddit_linkedin(reddit_results, linkedin_results):
    return f"Reddit Jobs:\n{reddit_results}\n\nLinkedIn Jobs:\n{linkedin_results}"


reddit_branch_chain = (
    RunnableLambda(lambda _: scrape_reddit_jobs()) | gemini_model | StrOutputParser()
)

linkedin_branch_chain = (
    RunnableLambda(lambda _: scrape_linkedin_jobs()) | gemini_model | StrOutputParser()
)

chain = RunnableParallel(
    branches={"reddit": reddit_branch_chain, "linkedin": linkedin_branch_chain}
) | RunnableLambda(
    lambda x: combine_reddit_linkedin(
        x["branches"]["reddit"], x["branches"]["linkedin"]
    )
)

result = chain.invoke({})

print(result)
