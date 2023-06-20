import fastapi
import uvicorn

from api import package_api
from api import stats_api
from infrastructure import mongo_setup

api = fastapi.FastAPI()


def main():
    configure_routing()

    # NO! Use @api.on_event('startup')
    # asyncio.run(mongo_setup.init_connection('pypi'))

    uvicorn.run(api)


def configure_routing():
    api.include_router(package_api.router)
    api.include_router(stats_api.router)


@api.on_event('startup')
async def configure_db():
    await mongo_setup.init_connection('pypi')


@api.get('/')
def hello_world():
    return {'message': "Greetings to the world!"}


if __name__ == '__main__':
    main()
else:
    configure_routing()
