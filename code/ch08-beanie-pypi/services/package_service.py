from typing import Optional

from beanie.odm.operators.find.array import ElemMatch

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


async def package_by_name(name: str) -> Optional[Package]:
    package = await Package.find_one(Package.id == name)
    return package


async def packages_with_version(major: int, minor: int, build: int) -> int:
    # noinspection PyUnresolvedReferences
    # Oops, not exactly!
    # packages_count = await Package.find(
    #     Package.releases.major_ver == major,# 1
    #     Package.releases.minor_ver == minor,# 2
    #     Package.releases.build_ver == build,
    # ).count()

    packages_count = await Package.find(
        ElemMatch(
            Package.releases,
            {"major_ver": major, "minor_ver": minor, "build_ver": build}
        )
    ).count()

    return packages_count
