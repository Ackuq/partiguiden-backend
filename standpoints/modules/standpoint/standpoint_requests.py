from django.http import Http404, HttpResponseBadRequest


from .standpoint_logic import create_standpoint, update_standpoint, lookup as lookup_logic


def lookup(request):
    if request.method == "GET":
        link = request.GET.get("link")
        if link is None:
            return HttpResponseBadRequest("Link field is blank")
        return lookup_logic(link=link)
    else:
        return Http404


def standpoint(request):
    if request.method == "POST":
        link = request.POST.get("link")
        party = request.POST.get("party")
        title = request.POST.get("title")
        content = request.POST.get("content")
        if link is None or party is None:
            return HttpResponseBadRequest("Link or party field is blank")
        return create_standpoint(link=link, party=party, title=title, content=content)
    elif request.method == "PUT":
        return update_standpoint(request)

    return Http404
