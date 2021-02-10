from typing import List

from .centerpartiet.get_pages import get_pages as get_pages_c
from .data_entry import DataEntry
from .kristdemokraterna.get_pages import get_pages as get_pages_kd
from .liberalerna.get_pages import get_pages as get_pages_l
from .miljopartiet.get_pages import get_pages as get_pages_mp
from .moderaterna.get_pages import get_pages as get_pages_m
from .socialdemokraterna.get_pages import get_pages as get_pages_s
from .sverigedemokraterna.get_pages import get_pages as get_pages_sd
from .vansterpartiet.get_pages import get_pages as get_pages_v


def get_party_data(abbreviation: str) -> List[DataEntry]:
    abbv_upper = abbreviation.lower()
    if abbv_upper == "S":
        return get_pages_s()
    elif abbv_upper == "M":
        return get_pages_m()
    elif abbv_upper == "C":
        return get_pages_c()
    elif abbv_upper == "KD":
        return get_pages_kd()
    elif abbv_upper == "L":
        return get_pages_l()
    elif abbv_upper == "MP":
        return get_pages_mp()
    elif abbv_upper == "SD":
        return get_pages_sd()
    elif abbv_upper == "V":
        return get_pages_v()
    else:
        return []
