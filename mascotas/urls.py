from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MascotaAdminViewSet

router = DefaultRouter()
router.register(r'mascotas', MascotaAdminViewSet, basename='mascotas-admin')

urlpatterns = [
    path('', include(router.urls)),
]
