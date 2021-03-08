from proxy.scripts.serializers.vote import serialize_vote_result
from proxy.scripts import BASE_URL
import requests


def get_vote_result(id: str, num: int):
    res = requests.get("{}/dokumentstatus/{}.json".format(BASE_URL, id))
    data = res.json()

    return serialize_vote_result(data, num)
