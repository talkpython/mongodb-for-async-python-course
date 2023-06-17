from typing import Optional

from models.user import User, Location


async def user_count() -> int:
    return await User.count()


async def create_user(name: str, email: str, password: str,
                      profile_image_url: Optional[str], location: Location) -> User:
    email = email.lower().strip()
    name = name.strip()
    password = password.strip()

    if await user_by_email(email):
        raise Exception(f"User already exists with {email}.")

    hash_password = None  # TODO: Derive this.
    user = User(name=name, email=email, hash_password=hash_password,
                profile_image_url=profile_image_url, location=location)

    await user.save()

    return user


async def user_by_email(email: str) -> Optional[User]:
    email = email.lower().strip()
    return await User.find_one(User.email == email)
