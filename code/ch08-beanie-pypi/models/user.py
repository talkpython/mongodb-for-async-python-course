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
    created_date: datetime.datetime
    last_login: datetime.datetime
    profile_image_url: Optional[str]
    location: Location
