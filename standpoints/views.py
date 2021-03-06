from hashlib import sha256
from typing import List

from django.db.models.manager import BaseManager
from django.http.response import HttpResponseBadRequest, HttpResponseNotFound
from django_filters.filters import BooleanFilter, CharFilter
from django_filters.filterset import FilterSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from standpoints.scripts.party_data.get_invalid_urls import get_invalid_urls

from .models import Party, Standpoint, Subject
from .scripts.party_data.get_party_data import get_party_data
from .serializer import PartySerializer, StandpointSerializer, SubjectSerializer


class StandpointFilter(FilterSet):
    party__abbreviation = CharFilter(lookup_expr="iexact")
    uncategorized = BooleanFilter(field_name="subject", lookup_expr="isnull")

    class Meta:
        model = Standpoint
        fields = ("party", "party__abbreviation", "subject")


class StandpointView(viewsets.ModelViewSet):
    queryset = Standpoint.objects.all()
    serializer_class = StandpointSerializer
    filterset_class = StandpointFilter

    def __purge_old(self, party) -> None:
        standpoints = Standpoint.objects.filter(party=party).values_list("id", "link")
        invalid_ids: List[str] = get_invalid_urls(list(standpoints))
        for invalid_id in invalid_ids:
            Standpoint.objects.get(pk=invalid_id).delete()

    def __handle_standpoints_update(self, abbreviation: str) -> BaseManager[Standpoint]:
        party = Party.objects.get(pk=abbreviation.upper())
        self.__purge_old(party)
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
                    id=id,
                    title=page.title,
                    content=page.opinions,
                    link=page.url,
                    party=party,
                )
        return Standpoint.objects.filter(party=party)

    @action(detail=False, permission_classes=[IsAdminUser])
    def update_standpoints(self, request):
        abbreviation: str = request.GET.get("party")
        if abbreviation is None:
            return Response(
                "Request must include a specific party",
                status=HttpResponseBadRequest.status_code,
            )
        try:
            if abbreviation.lower() == "all":
                all_abbreviations = list(Party.objects.values_list("abbreviation", flat=True))
                all_data = []
                for abbv in all_abbreviations:
                    queryset = self.__handle_standpoints_update(abbv)
                    serializer = self.get_serializer(queryset, many=True)
                    all_data += serializer.data
                return Response(all_data)
            else:
                queryset = self.__handle_standpoints_update(abbreviation)
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)

        except Party.DoesNotExist:
            return Response("Could not find specific party", status=HttpResponseNotFound.status_code)


class PartyView(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer


class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
