from django.db.models import QuerySet
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from .models import Party, Standpoint, Subject


class StandpointSerializer(ModelSerializer[Standpoint]):
    """Serializer for standpoints"""

    class Meta:
        model = Standpoint
        fields = ("id", "title", "content", "date", "link", "party", "subject")


class UpdatePartyStandpointsSerializer(ModelSerializer[Party]):
    """Serializer for updating party standpoints"""

    class Meta:
        model = Party
        fields = ()
        read_only_fields = ("id",)


class PartySerializer(ModelSerializer[Party]):
    """Serializer for parties"""

    class Meta:
        model = Party
        fields = ("id", "name")


class SubjectListSerializer(ModelSerializer[Subject]):
    """Serializer when listing subjects"""

    class Meta:
        model = Subject
        fields = ("id", "name", "related_subjects")


class RelatedSubjectIdsField(PrimaryKeyRelatedField[Subject]):
    """Special serializer for showing related subjects"""

    def get_queryset(self) -> QuerySet[Subject]:
        if "view" in self.context and hasattr(self.context["view"], "kwargs") and "pk" in self.context["view"].kwargs:
            return Subject.objects.all().exclude(pk=self.context["view"].kwargs["pk"])
        return Subject.objects.all()


class SubjectSerializer(ModelSerializer[Subject]):
    """Serializer for subjects"""

    standpoints = StandpointSerializer(many=True, read_only=True)
    related_subjects = SubjectListSerializer(many=True, read_only=True)
    related_subjects_ids = RelatedSubjectIdsField(many=True, write_only=True, source="related_subjects")

    class Meta:
        model = Subject
        fields = ("id", "name", "related_subjects", "standpoints", "related_subjects_ids")
