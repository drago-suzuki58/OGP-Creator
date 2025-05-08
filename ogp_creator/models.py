from sqlmodel import SQLModel, Field
from typing import Optional

import ogp_creator.utils as utils


class OGP(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path: str = Field(default_factory=utils.generate_random_path, index=True, unique=True)

    og_title: str = Field(default="")
    og_description: str = Field(default="")
    og_image: str = Field(default="")
    og_url: str = Field(default="")
