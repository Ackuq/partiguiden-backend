import logging
from datetime import date
from hashlib import sha256
from typing import List

from standpoints.models import Party, Standpoint

from .party_data.get_invalid_urls import get_invalid_urls
from .party_data.get_party_data import get_party_data

logger = logging.getLogger("standpoints")


def _purge_old(party) -> None:
    logger.info(f"Purging invalid urls for party {party}...")
    standpoints = Standpoint.objects.filter(party=party).values_list("id", "link")
    invalid_ids: List[str] = get_invalid_urls(list(standpoints))
    if len(invalid_ids) > 0:
        logger.warn("Found invalid ids: {}".format(invalid_ids))
        for invalid_id in invalid_ids:
            Standpoint.objects.filter(pk=invalid_id).delete()


def _handle_standpoints_update(party_id: str) -> None:
    party = Party.objects.get(pk=party_id.upper())
    logger.info(f"Updating standpoints for party {party_id}...")
    _purge_old(party)
    logger.info(f"Fetching new data for party {party_id}...")
    pages = get_party_data(party_id)
    logger.info(f"Found {len(pages)} for party {party_id}, writing new entries...")
    for page in pages:
        id = sha256(page.url.encode("utf-8")).hexdigest()
        try:
            logger.info(f"Updating existing entry {page.title} for party {party_id}")
            existing = Standpoint.objects.get(pk=id)
            existing.title = page.title
            existing.content = page.opinions
            existing.date = date.today()
            existing.save()
        except Standpoint.DoesNotExist:
            logger.info(f"Creating entry {page.title} for party {party_id}")
            Standpoint.objects.create(
                id=id,
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
