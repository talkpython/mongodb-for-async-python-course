import fastapi
import uvicorn
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from api import package_api
from api import stats_api
from infrastructure import mongo_setup

api = fastapi.FastAPI()
templates = Jinja2Templates(directory='templates')


def main():
    configure_routing()

    # NO! Use @api.on_event('startup')
    # asyncio.run(mongo_setup.init_connection('pypi'))

    uvicorn.run(api)


def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(package_api.router)
    api.include_router(stats_api.router)


@api.on_event('startup')
async def configure_db():
    dev_mode = True

    if dev_mode:
        await mongo_setup.init_connection('pypi')
    else:
        await mongo_setup.init_connection(
            'pypi', server='10.124.0.4', port=5621,
            username='pypi-database-user', password='9827a696-6cb9-47cc-a71e-e8b0ef38e2a3',
            use_ssl=True)


@api.get('/', include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse('index.html', {"name": "The app!", "request": request})


if __name__ == '__main__':
    main()
else:
    configure_routing()
