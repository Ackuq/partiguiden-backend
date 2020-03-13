from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from .standpoint_model import Standpoint
from ..party.party_model import Party


def lookup(link):
    try:
        standpoint = Standpoint.objects.get(link=link)
        return JsonResponse(model_to_dict(standpoint), safe=False)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Could not find standpoint")


def create_standpoint(link, party, title, content):
    if not Standpoint.objects.filter(link=link).exists():
        try:
            party_obj = Party.objects.get(name=party)
            standpoint = Standpoint(title=title, content=content, link=link, party=party_obj)
            standpoint.save()
            return JsonResponse(standpoint, safe=False)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Could not find party")
    else:
        return HttpResponseBadRequest("Standpoint already exisgs")


def update_standpoint(request):
    link = request.PUT.get("link")
    try:
        standpoint = Standpoint.objects.get(link=link)
        return JsonResponse(model_to_dict(standpoint))
    except Standpoint.DoesNotExist:
        return HttpResponseBadRequest("Object does not exist")
