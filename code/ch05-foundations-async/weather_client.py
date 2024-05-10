import asyncio
import datetime

import httpx

locations = [
    'https://weather.talkpython.fm/api/weather?city=New York&state=NY&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=Los Angeles&state=CA&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=Chicago&state=IL&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=Houston&state=TX&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=Phoenix&state=AZ&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=Philadelphia&state=PA&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=San Antonio&state=TX&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=San Diego&state=CA&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=Dallas&state=TX&country=US&units=imperial',
    'https://weather.talkpython.fm/api/weather?city=San Jose&state=CA&country=US&units=imperial',
]


async def get_report(url) -> dict:
    print(f"Calling {url}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

    return resp.json()


async def main_naive():
    t0 = datetime.datetime.now()
    for url in locations:
        report = await get_report(url)
        show_report(report)

    dt = datetime.datetime.now() - t0
    # Oops, recording has 100, should have been 1,000. But the ratios still hold the same.
    print(f"Done in {dt.total_seconds() * 1000:,.1f} ms.")


async def main():
    t0 = datetime.datetime.now()
    tasks = []
    for url in locations:
        tasks.append(asyncio.create_task(get_report(url)))

    for task in tasks:
        report = await task
        show_report(report)

    dt = datetime.datetime.now() - t0
    # Oops, recording has 100, should have been 1,000. But the ratios still hold the same.
    print(f"Done in {dt.total_seconds() * 1000:,.1f} ms.")


def show_report(report):
    print(report['forecast'], report['location'])


if __name__ == '__main__':
    asyncio.run(main_naive())
    asyncio.run(main())
