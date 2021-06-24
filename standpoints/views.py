from threading import Thread

from django.http.response import HttpResponseBadRequest, HttpResponseNotFound
from django_filters.filters import BooleanFilter, CharFilter
from django_filters.filterset import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Party, Standpoint, Subject
from .scripts.update_standpoints import update_standpoints
from .serializer import PartySerializer, StandpointSerializer, SubjectListSerializer, SubjectSerializer


class StandpointFilter(FilterSet):
    party__id = CharFilter(lookup_expr="iexact")
    uncategorized = BooleanFilter(field_name="subject", lookup_expr="isnull")

    class Meta:
        model = Standpoint
        fields = ("party", "party__id", "subject")


class StandpointView(viewsets.ModelViewSet):
    queryset = Standpoint.objects.all()
    serializer_class = StandpointSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["id", "title"]
    ordering = ["title"]
    filterset_class = StandpointFilter

    @action(detail=False, permission_classes=[IsAdminUser])
    def update_standpoints(self, request):
        party_id: str = request.GET.get("party")
        if party_id is None:
            return Response(
                "Request must include a specific party",
                status=HttpResponseBadRequest.status_code,
            )
        try:
            Thread(target=lambda: update_standpoints(party_id)).start()
            return Response("Your request was successful")

        except Party.DoesNotExist:
            return Response("Could not find specific party", status=HttpResponseNotFound.status_code)


class PartyView(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["id", "name"]
    ordering = ["name"]


class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ["id", "name"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return SubjectListSerializer
        else:
            return SubjectSerializer
