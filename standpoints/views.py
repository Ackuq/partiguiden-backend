import base64
import logging
from threading import Thread

from django.http import Http404
from django_filters.filters import BooleanFilter, CharFilter
from django_filters.filterset import FilterSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Party, Standpoint, Subject
from .scripts.update_standpoints import update_standpoints
from .serializer import (
    PartySerializer,
    StandpointSerializer,
    SubjectListSerializer,
    SubjectSerializer,
    UpdatePartyStandpointsSerializer,
)

logger = logging.getLogger(__name__)


class StandpointFilter(FilterSet):
    party__id = CharFilter(lookup_expr="iexact")
    uncategorized = BooleanFilter(field_name="subject", lookup_expr="isnull")

    class Meta:
        model = Standpoint
        fields = ("party", "party__id", "subject")


class StandpointView(viewsets.ModelViewSet):
    queryset = Standpoint.objects.all()
    serializer_class = StandpointSerializer
    filterset_class = StandpointFilter

    def get_object(self):
        # The ID supplied is a base64 version of the PK
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        try:
            self.kwargs[lookup_url_kwarg] = base64.b64decode(self.kwargs[lookup_url_kwarg]).decode("utf-8")
        except Exception:
            raise Http404
        return super().get_object()


class PartyView(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser],
        serializer_class=UpdatePartyStandpointsSerializer,
    )
    def update_standpoints(self, request, pk=None):
        party: Party = self.get_object()
        logger.info(f"Got request to update standpoints for party {pk}...")
        Thread(target=lambda: update_standpoints(party)).start()
        return Response("Your request was successful")


class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["name", "standpoints__title"]

    def get_serializer_class(self):
        if self.action == "list":
            return SubjectListSerializer
        else:
            return SubjectSerializer
