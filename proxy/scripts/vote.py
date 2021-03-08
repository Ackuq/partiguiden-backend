import requests

from proxy.scripts import BASE_URL
from proxy.scripts.serializers.vote import serialize_vote, serialize_vote_result


def get_vote_result(id: str, num: int):
    res = requests.get("{}/dokumentstatus/{}.json".format(BASE_URL, id))
    data = res.json()

    return serialize_vote_result(data, num)


def get_vote(id: str, proposition: int):
    res = requests.get("{}/dokumentstatus/{}.json".format(BASE_URL, id))
    data = res.json()

    return serialize_vote(data, proposition)
