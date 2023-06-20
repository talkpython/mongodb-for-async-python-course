import fastapi

from models.package import Package
from services import package_service

router = fastapi.APIRouter()


@router.get('/api/packages/recent/{count}')
async def recent(count: int):
    return {"count": count}


@router.get('/api/packages/details/{name}', response_model=Package)
async def details(name: str):
    package = await package_service.package_by_name(name)
    if package is None:
        return fastapi.responses.JSONResponse({'error': f'Package {name} not found'}, status_code=404)

    return package
