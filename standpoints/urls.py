from .modules.party.party_urls import party_urls
from .modules.subject.subject_urls import subject_urls
from .modules.standpoint.standpoint_url import standpoint_urls

urlpatterns = party_urls + subject_urls + standpoint_urls
