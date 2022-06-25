import asyncio
from time import sleep
from typing import List, Tuple

import aiohttp


def get_or_create_event_loop() -> asyncio.AbstractEventLoop:
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
        raise ex


async def _check_url(id: str, url: str) -> Tuple[str, bool]:
    """
    Returns tuple `(id, is_ok)`. Will get removed if `is_ok` is `False`.
    """
    # Sleep so we do not get rate limited :)
    sleep(0.1)
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        await resp.text()
        return id, resp.ok


def get_invalid_urls(standpoints: List[Tuple[str, str]]) -> List[str]:
    """
    Takes a list of tuples of the form (id, url) and outputs a list of standpoints with invalid urls
    """
    loop = get_or_create_event_loop()
    futures = asyncio.gather(*[_check_url(id, url) for id, url in standpoints])
    data = loop.run_until_complete(futures)
    invalid = [id for id, is_ok in data if is_ok is False]
    return invalid
