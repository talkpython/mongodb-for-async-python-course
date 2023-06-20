import fastapi

router = fastapi.APIRouter()


@router.get('/api/packages/recent/{count}')
async def recent(count: int):
    return {"count": count}


@router.get('/api/packages/details/{name}')
async def details(name: str):
    return {"Package": name}
