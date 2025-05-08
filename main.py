from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

import ogp_creator.db as db
import ogp_creator.routers as routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield
    pass

app = FastAPI(lifespan=lifespan)

app.mount("/statics", StaticFiles(directory="statics"), name="statics")
templates = Jinja2Templates(directory="templates")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)