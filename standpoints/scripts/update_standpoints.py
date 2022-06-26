import logging
from datetime import date
from typing import List

from standpoints.models import Party, Standpoint

from .party_data.get_invalid_urls import get_invalid_urls
from .party_data.get_party_data import get_party_data

logger = logging.getLogger("standpoints")


def _purge_old(party) -> None:
    logger.info(f"Purging invalid urls for party {party}...")
    standpoints = list(Standpoint.objects.filter(party=party).values_list("link", flat=True))
    invalid_urls: List[str] = get_invalid_urls(standpoints)
    if len(invalid_urls) > 0:
        logger.warn("Found invalid ids: {}".format(invalid_urls))
        for invalid_url in invalid_urls:
            Standpoint.objects.filter(pk=invalid_url).delete()


def _handle_standpoints_update(party_id: str) -> None:
    party = Party.objects.get(pk=party_id.upper())
    logger.info(f"Updating standpoints for party {party_id}...")
    _purge_old(party)
    logger.info(f"Fetching new data for party {party_id}...")
    pages = get_party_data(party_id)
    logger.info(f"Found {len(pages)} for party {party_id}, writing new entries...")
    for page in pages:
        try:
            existing = Standpoint.objects.get(pk=page.url)
            logger.info(f"Updating existing entry {page.title} for party {party_id}")
            existing.title = page.title
            existing.content = page.opinions
            existing.date = date.today()
            existing.save()
        except Standpoint.DoesNotExist:
            logger.info(f"Creating entry {page.title} for party {party_id}")
            Standpoint.objects.create(
                title=page.title,
                content=page.opinions,
                link=page.url,
                party=party,
            )


def update_standpoints(party_id: str) -> None:
    if party_id.lower() == "all":
        all_ids = list(Party.objects.values_list("id", flat=True))
        for id in all_ids:
            _handle_standpoints_update(id)
    else:
        _handle_standpoints_update(party_id)
