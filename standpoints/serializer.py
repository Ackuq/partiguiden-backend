from rest_framework import serializers

from .models import Party, Standpoint, Subject


class StandpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standpoint
        fields = ("id", "title", "content", "date", "link", "party", "subject")


class PartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Party
        fields = ("id", "name")


class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name")


class RelatedSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name")


class SubjectSerializer(serializers.ModelSerializer):
    standpoints = StandpointSerializer(many=True, read_only=True)
    related_subject = RelatedSubjectSerializer(many=True)

    class Meta:
        model = Subject
        fields = ("id", "name", "related_subject", "standpoints")
