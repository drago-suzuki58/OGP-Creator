from fastapi import APIRouter, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import Request
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from ogp_creator.db import get_session
import ogp_creator.env as env
from ogp_creator.limiter import limiter
import ogp_creator.models as models
import ogp_creator.schemas as schemas


meta_router = APIRouter(prefix="", tags=["Meta"])

@meta_router.get("/robots.txt", response_class=FileResponse)
@limiter.limit("100/hour")
async def get_robots_txt(request: Request):
    return FileResponse("statics/robots.txt")


root_router = APIRouter(prefix="", tags=["Root"])
templates = Jinja2Templates(directory="templates")

@root_router.get("/")
@limiter.limit("50/minute")
async def get_root_template(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "year": env.YEAR,
        "creator_name": env.CREATER_NAME,
        "github_link": env.GITHUB_LINK
    })

@root_router.get("/{path}", response_class=HTMLResponse)
@limiter.limit("20/minute")
async def get_ogp_template(request: Request, path: str):
    with get_session() as session:
        query = select(models.OGP).where(models.OGP.path == path)
        ogp = session.exec(query).first()

        if not ogp:
            raise HTTPException(status_code=404, detail="OGP not found.")

    return templates.TemplateResponse("ogp.html", {
        "request": request,
        "og_title": ogp.og_title,
        "og_description": ogp.og_description,
        "og_image": ogp.og_image,
        "og_url": ogp.og_url,
        "year": env.YEAR,
        "creator_name": env.CREATER_NAME,
        "github_link": env.GITHUB_LINK
    })


api_router = APIRouter(prefix="/api", tags=["API"])

@api_router.post("/ogp")
@limiter.limit("3/minute")
async def create_ogp(request: Request, ogp_schema: schemas.OGP):
    if ogp_schema.path in env.RESERVED_PATHS:
        raise HTTPException(status_code=400, detail=f"The path '{ogp_schema.path}' is reserved and cannot be used.")

    # ここで全部strに変換されるため、これで問題なし
    ogp = models.OGP(
        path=ogp_schema.path, # type: ignore
        og_title=ogp_schema.og_title, # type: ignore
        og_description=ogp_schema.og_description, # type: ignore
        og_image=ogp_schema.og_image, # type: ignore
        og_url=ogp_schema.og_url # type: ignore
    )

    with get_session() as session:
        try:
            session.add(ogp)
            session.commit()
            session.refresh(ogp)
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=400, detail=f"The path '{ogp_schema.path}' is already exists.")

    return {"message": "OGP created successfully", "ogp": ogp}

@api_router.get("/ogp")
@limiter.limit("10/minute")
async def get_ogp(request: Request, path: str = Query(...)):
    with get_session() as session:
        query = select(models.OGP).where(models.OGP.path == path)
        ogp = session.exec(query).first()

        if not ogp:
            raise HTTPException(status_code=404, detail="OGP not found.")

    return {"ogp": ogp}
