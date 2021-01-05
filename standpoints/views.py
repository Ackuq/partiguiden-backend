from hashlib import sha256

from django.http.response import HttpResponseBadRequest, HttpResponseNotFound
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Party, Standpoint, Subject
from .scripts.party_data.get_party_data import get_party_data
from .serializer import PartySerializer, StandpointSerializer, SubjectSerializer


class StandpointFilter(filters.FilterSet):
    party__abbreviation = filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Standpoint
        fields = ("party", "party__abbreviation", "subject")


class StandpointView(viewsets.ModelViewSet):
    queryset = Standpoint.objects.all()
    serializer_class = StandpointSerializer
    filterset_class = StandpointFilter

    @action(detail=False, permission_classes=[IsAdminUser])
    def update_standpoints(self, request):
        abbreviation = request.GET.get("party")
        if abbreviation is None:
            return Response("Request must include a specific party", status=HttpResponseBadRequest.status_code)

        try:
            party = Party.objects.get(pk=abbreviation)
            pages = get_party_data(abbreviation)

            for page in pages:
                id = sha256(page.url.encode("utf-8")).hexdigest()

                try:
                    existing = Standpoint.objects.get(pk=id)
                    existing.title = page.title
                    existing.content = page.opinions
                    existing.save()
                except Standpoint.DoesNotExist:
                    Standpoint.objects.create(
                        id=id, title=page.title, content=page.opinions, link=page.url, party=party
                    )

        except Party.DoesNotExist:
            return Response("Could not find specific party", status=HttpResponseNotFound.status_code)

        queryset = Standpoint.objects.filter(party=party)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PartyView(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer


class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
