import datetime
from typing import Optional

import pydantic


# Goal of this step:
# Start modeling with just pydantic
# We'll evolve this into beanie in the next step.

def main():
    print("Creating new user...")

    # TODO: Make sure you set up the DB connection before this line.
    loc = Location(city="Portland", state="OR", country="USA")
    user = User(name="Michael", email="michael@talkpython.fm", location=loc)

    print(user)

    print("Done.")


class Location(pydantic.BaseModel):
    city: str
    state: str
    country: str


class User(pydantic.BaseModel):  # beanie.Document):
    name: str
    email: str
    password_hash: Optional[str]

    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    last_login: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)

    location: Location


if __name__ == '__main__':
    main()
