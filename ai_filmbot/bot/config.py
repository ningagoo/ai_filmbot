import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    CHANNEL_IDS = list(map(int, os.getenv("CHANNELS", "").split(","))) if os.getenv("CHANNELS") else []

    CHANNEL_LINKS = os.getenv("CHANNEL_LINKS", "").split(",") if os.getenv("CHANNEL_LINKS") else []

config = Config()