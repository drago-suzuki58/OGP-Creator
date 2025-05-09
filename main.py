from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import logging
from logging.handlers import TimedRotatingFileHandler

import ogp_creator.db as db
import ogp_creator.env as env
import ogp_creator.routers as routers

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s\t: %(name)s\t: %(levelname)s\t: %(message)s",
    handlers=[
        TimedRotatingFileHandler(
            "logs/app.log",
            when="midnight",
            interval=1,
            backupCount=30
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    logger.info("Database initialized.")
    yield
    logger.info("Application shutdown.")

app = FastAPI(lifespan=lifespan)

app.mount("/statics", StaticFiles(directory="statics"), name="statics")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

app.include_router(routers.meta_router)
app.include_router(routers.root_router)
app.include_router(routers.api_router)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting application...")
    uvicorn.run(
        "main:app",
        host=env.IP,
        port=int(env.PORT),
        reload=True,
        reload_excludes=["logs/"]
    )
