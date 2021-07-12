from rest_framework import serializers

from .models import Party, Standpoint, Subject


class StandpointSearchSerializer(serializers.ModelSerializer):
    """Serializer when searching standpoints"""

    class Meta:
        model = Standpoint
        fields = ("id", "title", "subject")


class StandpointSerializer(serializers.ModelSerializer):
    """Serializer for standpoints"""

    class Meta:
        model = Standpoint
        fields = ("id", "title", "content", "date", "link", "party", "subject")


class PartySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for parties"""

    class Meta:
        model = Party
        fields = ("id", "name")


class SubjectListSerializer(serializers.ModelSerializer):
    """Serializer when listing subjects"""

    class Meta:
        model = Subject
        fields = ("id", "name", "related_subjects")


class RelatedSubjectIdsField(serializers.PrimaryKeyRelatedField):
    """Special serializer for showing related subjects"""

    def get_queryset(self):
        if "view" in self.context and hasattr(self.context["view"], "kwargs") and "pk" in self.context["view"].kwargs:
            return Subject.objects.all().exclude(pk=self.context["view"].kwargs["pk"])
        return Subject.objects.all()


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for subjects"""

    standpoints = StandpointSerializer(many=True, read_only=True)
    related_subjects = SubjectListSerializer(many=True, read_only=True)
    related_subjects_ids = RelatedSubjectIdsField(many=True, write_only=True, source="related_subjects")

    class Meta:
        model = Subject
        fields = ("id", "name", "related_subjects", "standpoints", "related_subjects_ids")
