from sqlmodel import SQLModel
from typing import Optional


class OGP(SQLModel):
    path: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    og_url: Optional[str] = None
