import asyncio

from infrastructure import mongo_setup
from models.user import Location
from services import package_service, user_service


async def main():
    print_header()

    await mongo_setup.init_connection('pypi')
    print()
    await summary()

    while True:
        print("[s] Show summary statistics")
        print("[f] Search the database for packages")
        print("[p] Most recently updated packages")
        print("[u] Create a new user")
        print("[r] Create a release")
        print("[x] Exit program")
        resp = input("Enter the character for your command: ").strip().lower()
        print('-' * 40)

        match resp:
            case 's':
                await summary()
            case 'f':
                await search_for_package()
            case 'p':
                await recently_updated()
            case 'u':
                await create_user()
            case 'r':
                await create_release()
            case 'x':
                break
            case _:
                print("Sorry, we don't understand that command.")

        print()  # give the output a little room each time.

    print('bye!')


def print_header():
    pad = 30
    print('/' + "-" * pad + '\\')
    print('|' + ' ' * pad + '|')
    print('|        PyPI CLI v1.0 ' + ' ' * (pad - 22) + '|')
    print('|' + ' ' * pad + '|')
    print('\\' + "-" * pad + '/')
    print()


async def summary():
    package_count = await package_service.package_count()
    release_count = await package_service.release_count()
    user_count = await user_service.user_count()

    print('PyPI Package Stats')
    print(f'Packages: {package_count:,}')
    print(f'Releases: {release_count:,}')
    print(f'Users: {user_count:,}')
    print()


async def search_for_package():
    print("Let's find some packages")
    name = input("Enter the exact name of a package to find: ").lower().strip()

    package = await package_service.package_by_name(name)
    if package:
        print(f'Found {package.id}, last updated: {package.last_updated.date().isoformat()}, with '
              f'{len(package.releases):,} releases.')
    else:
        print(f"No package with ID {name} found.")

    print("Now let's find packages with a certain release.")
    text = input("Enter version text in the format 1.2.3: ")
    parts = text.strip().split('.')
    major = int(parts[0])
    minor = int(parts[1])
    build = int(parts[2])

    package_count = await package_service.packages_with_version(major, minor, build)
    print(f'We found {package_count:,} packages with version {major}.{minor}.{build}')

    print()


async def recently_updated():
    packages = await package_service.recently_updated()
    for n, p in enumerate(packages, start=1):
        print(f'{n}. {p.id} ({p.last_updated.date().isoformat()}) - {p.summary[:80]}')
    print()


async def create_user():
    print("Create new user:")
    name = input("What is the user's full name: ")
    email = input("What is the user's email: ")
    if await user_service.user_by_email(email):
        print(f"Error: A user with the email {email} already exists, cancelling.")
        return

    password = input("Enter the password: ")
    state = input("Enter state or providence: ")
    country = input("Enter country: ")

    location = Location(state=state, country=country)
    user = await user_service.create_user(name, email, password, None, location)

    print(f"Created {user.name} ({user.email}) with ID {user.id}")


async def create_release():
    print("Create a release")
    name = input("Enter the name of the package for the release: ")

    package = await package_service.package_by_name(name)
    if not package:
        print(f"Error: Package with name {name} not found.")
        return

    print(f"Ok, we'll need some info about the release for {name}")
    version_text = input("Version (e.g. 1.2.3): ")
    v_parts = version_text.strip().split(".")
    major, minor, build = int(v_parts[0]), int(v_parts[1]), int(v_parts[2])

    comment = input("Comment about this release: ").strip()
    size = int(input("Size in bytes: "))
    url = input("Url for release notes (optional - enter to skip): ") or None

    await package_service.create_release(major, minor, build, name, comment, size, url)
    print(f"Release added for {version_text} of {name}.")


if __name__ == '__main__':
    asyncio.run(main())
