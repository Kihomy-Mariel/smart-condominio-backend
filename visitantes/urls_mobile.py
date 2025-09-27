from rest_framework.routers import DefaultRouter
from .views import PublicVisitanteViewSet

router = DefaultRouter()
router.register(r"mobile/visitantes", PublicVisitanteViewSet, basename="visitante-mobile")

urlpatterns = router.urls
