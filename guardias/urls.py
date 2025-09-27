from rest_framework.routers import DefaultRouter
from .views import GuardiaViewSet

router = DefaultRouter()
router.register(r"guardias", GuardiaViewSet, basename="guardia")

urlpatterns = router.urls
