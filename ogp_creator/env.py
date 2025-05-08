import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./data/ogp.db"
RESERVED_PATHS = os.getenv("RESERVED_PATHS", "").split(",") or ["admin", "api", "dashboard", "404", "403", ""]
