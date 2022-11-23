from django.contrib.admin import ModelAdmin, register

from .models import Party, Standpoint, Subject


@register(Standpoint)
class StandpointAdmin(ModelAdmin[Standpoint]):
    list_display = ["title", "link", "party"]
    list_filter = ["party"]
    readonly_fields = ["date"]


@register(Party)
class PartyAdmin(ModelAdmin[Party]):
    pass


@register(Subject)
class SubjectAdmin(ModelAdmin[Subject]):
    pass
