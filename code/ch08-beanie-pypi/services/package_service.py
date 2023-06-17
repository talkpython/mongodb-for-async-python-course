from models.package import Package
from models.release_analytics import ReleaseAnalytics


async def package_count() -> int:
    return await Package.count()


async def release_count() -> int:
    analytics = await ReleaseAnalytics.find_one()
    if not analytics:
        print("ERROR: No analytics?")
        return 0

    return analytics.total_releases
