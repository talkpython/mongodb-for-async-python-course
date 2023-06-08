import asyncio
import datetime
from typing import Optional

import beanie
import motor.motor_asyncio
import pydantic


# Goal of this step:
# Connect to MongoDB with Beanie.
# We'll evolve this into beanie in the next step.

async def main():
    await init_connection('beanie_quickstart')
    await create_a_user()
    await insert_multiple_users()

    print("Done.")


async def init_connection(db_name: str):
    conn_str = f"mongodb://localhost:27017/{db_name}"
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)

    await beanie.init_beanie(database=client[db_name], document_models=[User])

    print(f"Connected to {db_name}.")


async def create_a_user():
    user_count = await User.count()
    if user_count > 0:
        print(f"Already have {user_count:,} users!")
        return

    print("Creating new user...")
    # Make sure you set up the DB connection before this line.
    loc = Location(city="Portland", state="OR", country="USA")
    user = User(name="Michael", email="michael@talkpython.fm", location=loc)
    print(f'User before save: {user}')

    await user.save()

    print(f'User after save: {user}')


async def insert_multiple_users():
    user_count = await User.count()
    if user_count >= 4:
        print(f"Already have {user_count:,} users!")
        return

    print("Creating a set of users ...")

    # Make sure you set up the DB connection before this line.
    u1 = User(name="Michael", email='michael@talkpython.fm', location=Location(state='Oregon', country='USA'))
    u2 = User(name="Sarah", email='sarah@talkpython.fm', location=Location(state='Tennessee', country='USA'))
    u3 = User(name="Kylie", email='k@talkpython.fm', location=Location(state='Baden-Württemberg', country='Germany'))

    await User.insert_many([u1, u2, u3])

    print('Inserted multiple users objects.')


class Location(pydantic.BaseModel):
    city: Optional[str]
    state: str
    country: str


class User(beanie.Document):
    name: str
    email: str
    password_hash: Optional[str]

    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    last_login: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)

    location: Location


if __name__ == '__main__':
    asyncio.run(main())
