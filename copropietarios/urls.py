from rest_framework.routers import DefaultRouter
from .views import CopropietarioViewSet

router = DefaultRouter()
router.register(r"copropietarios", CopropietarioViewSet, basename="copropietario")

urlpatterns = router.urls
