from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("standpoints", views.StandpointView)
router.register("parties", views.PartyView)
router.register("subjects", views.SubjectView)

urlpatterns = router.urls
