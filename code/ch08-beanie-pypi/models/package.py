import datetime
from typing import Optional

import beanie as beanie
import bson
import pydantic


class Release(pydantic.BaseModel):
    major_ver: int
    minor_ver: int
    build_ver: int
    created_date: str
    comment: Optional[str]
    url: str
    size: int


class Package(beanie.Document):
    created_date: datetime.datetime
    last_updated: datetime.datetime
    summary: str
    description: str
    home_page: Optional[str]
    docs_url: Optional[str]
    package_url: Optional[str]
    author_name: Optional[str]
    author_email: Optional[str]
    license: Optional[str]
    releases: list[Release]
    maintainer_ids: list[bson.ObjectId]
