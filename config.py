import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(__file__)

DATABASE_DIR = os.path.join(BASE_DIR, "database")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

APP_NAME = "Pharma AI"
APP_VERSION = "0.4.0"