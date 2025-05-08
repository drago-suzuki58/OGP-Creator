from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

import ogp_creator.db as db
import ogp_creator.env as env
import ogp_creator.routers as routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield
    pass

app = FastAPI(lifespan=lifespan)

app.mount("/statics", StaticFiles(directory="statics"), name="statics")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

app.include_router(routers.api_router)
app.include_router(routers.root_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=env.IP, port=int(env.PORT), reload=True)
