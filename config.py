import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
DB_HOST=os.environ.get("DB_HOST")
DB_PORT=os.environ.get("DB_PORT")
DB_NAME=os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD=os.environ.get("DB_PASSWORD")
TOKEN_BOT=os.environ.get("ACCESS_TOKEN_BOT")
CHAT_ID = os.environ.get("CHAT_ID")
