import asyncio

from infrastructure import mongo_setup
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
    print("create_user")


async def create_release():
    print("create_release")


if __name__ == '__main__':
    asyncio.run(main())
