from hashlib import sha256
from typing import List

from standpoints.models import Party, Standpoint

from .party_data.get_invalid_urls import get_invalid_urls
from .party_data.get_party_data import get_party_data


def _purge_old(party) -> None:
    standpoints = Standpoint.objects.filter(party=party).values_list("id", "link")
    invalid_ids: List[str] = get_invalid_urls(list(standpoints))
    print("Found invalid ids: {}".format(invalid_ids))
    for invalid_id in invalid_ids:
        Standpoint.objects.filter(pk=invalid_id).delete()


def _handle_standpoints_update(party_id: str) -> None:
    party = Party.objects.get(pk=party_id.upper())
    _purge_old(party)
    pages = get_party_data(party_id)

    for page in pages:
        id = sha256(page.url.encode("utf-8")).hexdigest()

        try:
            existing = Standpoint.objects.get(pk=id)
            existing.title = page.title
            existing.content = page.opinions
            existing.save()
        except Standpoint.DoesNotExist:
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
