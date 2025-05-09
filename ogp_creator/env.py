import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ogp.db")
RESERVED_PATHS = os.getenv("RESERVED_PATHS", "").split(",") or ["api", "statics", "assets", "robots.txt", ""]
PORT = int(os.getenv("PORT", "8000"))
IP = os.getenv("IP", "0.0.0.0")
RELOAD = os.getenv("RELOAD", "False").lower() == "true"

YEAR = os.getenv("YEAR", "2025")
CREATER_NAME = os.getenv("CREATER_NAME", "drago-suzuki58")
GITHUB_LINK = os.getenv("GITHUB_LINK", "https://github.com/drago-suzuki58/OGP-Creator")
