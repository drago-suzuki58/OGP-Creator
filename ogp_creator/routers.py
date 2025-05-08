from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from ogp_creator.db import get_session
import ogp_creator.env as env
import ogp_creator.models as models
import ogp_creator.schemas as schemas


api_router = APIRouter(prefix="/api", tags=["API"])

@api_router.post("/ogp")
async def create_ogp(ogp_schema: schemas.OGP):
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
async def get_ogp(path: str = Query(...)):
    with get_session() as session:
        query = select(models.OGP).where(models.OGP.path == path)
        ogp = session.exec(query).first()

        if not ogp:
            raise HTTPException(status_code=404, detail="OGP not found.")

    return {"ogp": ogp}
