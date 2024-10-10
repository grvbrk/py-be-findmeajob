import discord
import asyncio
from discord.ext import commands
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

job_keywords = [
    "hiring",
    "job opening",
    "job opportunity",
    "looking for",
    "recruit",
    "position available",
    "apply now",
    "job application",
    "career opportunity",
    "seeking",
    "developer needed",
    "programmer wanted",
    "software engineer",
]


async def scrape_channels(guild):
    job_posts = []
    for channel in guild.text_channels:
        try:
            async for message in channel.history(limit=100):
                content = message.content.lower()
                if any(keyword in content for keyword in job_keywords):
                    job_posts.append(
                        {
                            "content": message.content,
                            "author": str(message.author),
                            "channel": str(channel),
                            "created_at": message.created_at.isoformat(),
                            "url": message.jump_url,
                        }
                    )
        except discord.errors.Forbidden:
            print(f"No access to channel: {channel}")
    return job_posts


async def scrape_and_print():
    all_job_posts = []
    for guild in bot.guilds:
        job_posts = await scrape_channels(guild)
        all_job_posts.extend(job_posts)

    print(f"Found {len(all_job_posts)} job-related posts")

    return all_job_posts


async def scheduled_scraping():
    while True:
        print(f"Starting scraping process at {datetime.datetime.now()}")
        await scrape_and_print()
        print(f"Scraping completed. Waiting for 1 hour before next scrape.")
        await asyncio.sleep(3600)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    bot.loop.create_task(scheduled_scraping())


bot.run(token=os.getenv("DISCORD_BOT_TOKEN"))
