from django.contrib.admin import ModelAdmin, register

from .models import Party, Standpoint, Subject


@register(Standpoint)
class StandpointAdmin(ModelAdmin):  # type: ignore
    list_display = ["title", "link", "party"]
    list_filter = ["party"]
    readonly_fields = ["date"]


@register(Party)
class PartyAdmin(ModelAdmin):  # type: ignore
    pass


@register(Subject)
class SubjectAdmin(ModelAdmin):  # type: ignore
    pass
