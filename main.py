from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import logging
from logging.handlers import TimedRotatingFileHandler

import ogp_creator.db as db
import ogp_creator.env as env
from ogp_creator.limiter import limiter
import ogp_creator.routers as routers


os.makedirs("logs", exist_ok=True)

if env.RELOAD is False:
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None
    )
app.state.limiter = limiter

app.mount("/statics", StaticFiles(directory="statics"), name="statics")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

app.include_router(routers.meta_router)
app.include_router(routers.root_router)
app.include_router(routers.api_router)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=429,
            content={
                "detail": "You have exceeded the allowed number of requests. Please try again later."
            }
        )
    else:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "You have exceeded the allowed number of requests.",
            "suggestion": "Please wait a moment and try again."
        }, status_code=429)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=env.IP,
        port=env.PORT,
        reload=env.RELOAD,
        reload_excludes=["logs/"]
    )
