from django.http import JsonResponse, HttpResponseNotFound

from .standpoint_model import Standpoint


def lookup(request):
    link = request.GET.get("link")
    standpoints = Standpoint.objects.filter(link=link)
    if standpoints.exists():
        standpoint = standpoints.values().first()
        print(standpoint)
        return JsonResponse(standpoint, safe=False)
    else:
        return HttpResponseNotFound("Could not find standpoint")
