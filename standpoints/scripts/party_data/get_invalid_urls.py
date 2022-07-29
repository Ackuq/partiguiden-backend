import asyncio
import logging
from random import randint
from typing import List, Tuple

import aiohttp

logger = logging.getLogger(__name__)


def get_or_create_event_loop() -> asyncio.AbstractEventLoop:
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
        raise ex


async def _check_url(url: str) -> Tuple[str, bool]:
    """
    Returns tuple `(url, is_ok)`. Will get removed if `is_ok` is `False`.
    """
    # Sleep so we do not get rate limited :)
    await asyncio.sleep(randint(1, 1000) / 10)
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        await resp.text()
        if not resp.ok:
            logger.warn(f"Got status {resp.status} when fetching URL {url}")
        return url, resp.ok


def get_invalid_urls(standpoints: List[str]) -> List[str]:
    """
    Takes a list of tuples of the form (id, url) and outputs a list of standpoints with invalid urls
    """
    loop = get_or_create_event_loop()
    futures = asyncio.gather(*[_check_url(url) for url in standpoints])
    data = loop.run_until_complete(futures)
    invalid = [id for id, is_ok in data if is_ok is False]
    return invalid
