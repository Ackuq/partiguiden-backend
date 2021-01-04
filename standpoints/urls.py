from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("standpoints", views.StandpointView)
router.register("parties", views.PartyView)
router.register("subjects", views.SubjectView)

urlpatterns = router.urls
