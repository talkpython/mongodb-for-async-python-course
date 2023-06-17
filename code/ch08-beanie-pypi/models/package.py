import datetime
from typing import Optional

import beanie as beanie
import pydantic


class Release(pydantic.BaseModel):
    major_ver: int
    minor_ver: int
    build_ver: int
    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    comment: Optional[str]
    url: Optional[str]
    size: int


class Package(beanie.Document):
    id: str
    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    last_updated: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    summary: str
    description: str
    home_page: Optional[str]
    docs_url: Optional[str]
    package_url: Optional[str]
    author_name: Optional[str]
    author_email: Optional[str]
    license: Optional[str]
    releases: list[Release]
    maintainer_ids: list[beanie.PydanticObjectId]

    class Settings:
        name = 'packages'
        indexes = []
