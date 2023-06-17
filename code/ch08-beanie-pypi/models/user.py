import datetime
from typing import Optional

import beanie
import pydantic


class Location(pydantic.BaseModel):
    state: Optional[str]
    country: Optional[str]


class User(beanie.Document):
    name: str
    email: str
    hash_password: Optional[str]
    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    last_login: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    profile_image_url: Optional[str]
    location: Location

    class Settings:
        name = 'users'
        indexes = []
