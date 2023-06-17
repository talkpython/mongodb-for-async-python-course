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


async def recently_updated(count=5):
    # noinspection PyUnresolvedReferences
    updated = await Package.find_all().sort(-Package.last_updated).limit(count).to_list()

    return updated
