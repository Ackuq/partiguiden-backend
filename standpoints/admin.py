from django.contrib import admin

from .models import Party, Standpoint, Subject


@admin.register(Standpoint)
class StandpointAdmin(admin.ModelAdmin):
    list_filter = ["party"]
    readonly_fields = ["date"]


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass
