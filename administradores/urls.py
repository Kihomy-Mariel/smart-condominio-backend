# administradores/urls.py
from rest_framework.routers import DefaultRouter
from .views import AdministradorViewSet

router = DefaultRouter()
router.register(r"admins", AdministradorViewSet, basename="admin")

urlpatterns = router.urls
