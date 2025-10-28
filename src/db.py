from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("DB_URL")

print(url)
