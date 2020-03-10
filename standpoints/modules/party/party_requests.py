from django.http import JsonResponse

from .party_model import Party
from ..standpoint.standpoint_model import Standpoint


def get_parties(request):
    parties = Party.objects.values()
    party_list = list(parties)
    return JsonResponse(party_list, safe=False)


# Get all the party standpoints
def get_party_standpoint(request, party):
    party_standpoints = Standpoint.objects.filter(party__abbreviation=party).values()
    standpoint_list = list(party_standpoints)
    return JsonResponse(standpoint_list, safe=False)
