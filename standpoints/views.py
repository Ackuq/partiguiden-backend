from rest_framework import viewsets
from .models import Standpoint, Party, Subject
from .serializer import StandpointSerializer, PartySerializer, SubjectSerializer
from django_filters import rest_framework as filters


class StandpointFilter(filters.FilterSet):
    party__abbreviation = filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Standpoint
        fields = ("party", "party__abbreviation", "subject")


class StandpointView(viewsets.ModelViewSet):
    queryset = Standpoint.objects.all()
    serializer_class = StandpointSerializer
    filterset_class = StandpointFilter


class PartyView(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer


class SubjectView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
