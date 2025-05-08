import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ogp.db")
RESERVED_PATHS = os.getenv("RESERVED_PATHS", "").split(",") or ["admin", "api", "dashboard", "404", "403", ""]

YEAR = os.getenv("YEAR", "2025")
CREATER_NAME = os.getenv("CREATER_NAME", "drago-suzuki58")
GITHUB_LINK = os.getenv("GITHUB_LINK", "https://github.com/drago-suzuki58/OGP-Creator")
