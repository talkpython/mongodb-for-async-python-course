import fastapi
import uvicorn

from api import package_api
from api import stats_api

api = fastapi.FastAPI()


def main():
    configure_routing()
    uvicorn.run(api)


def configure_routing():
    api.include_router(package_api.router)
    api.include_router(stats_api.router)


@api.get('/')
def hello_world():
    return {'message': "Greetings to the world!"}


if __name__ == '__main__':
    main()
else:
    configure_routing()
