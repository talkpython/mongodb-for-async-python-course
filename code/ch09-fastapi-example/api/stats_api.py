import fastapi

router = fastapi.APIRouter()


@router.get('/api/stats')
async def stats():
    return {"stats": 1}
