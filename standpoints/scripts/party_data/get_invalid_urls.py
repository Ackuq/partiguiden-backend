from typing import List, Tuple

import requests


def get_invalid_urls(standpoints: List[Tuple[str, str]]) -> List[str]:
    """
    Takes a list of tuples of the form (id, url) and outputs a list of standpoints with invalid urls
    """
    invalid: List[str] = []
    for (id, url) in standpoints:
        try:
            res = requests.get(url, timeout=10)
            if not res.ok:
                invalid.append(id)
        except TimeoutError:
            invalid.append(id)
    return invalid
