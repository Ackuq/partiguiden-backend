from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path("decisions/", views.DecisionsView.as_view()),
    path("documents/member/<slug:id>", views.MemberDocumentsView.as_view()),
    path("documents/json/<slug:id>/", views.JSONDocumentView.as_view()),
    path("documents/html/<slug:id>/", views.MemberDocumentsView.as_view()),
    path("member/<slug:id>/", views.MemberView.as_view()),
    path("members/", views.MembersView.as_view()),
    path("member/", views.MemberSearchView.as_view()),
    path("party/<str:party>", views.PartyView.as_view()),
    path("votes/", views.VotesView.as_view()),
]

urlpatterns += router.urls
