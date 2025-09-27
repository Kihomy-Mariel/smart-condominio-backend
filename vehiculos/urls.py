from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculoAdminViewSet

router = DefaultRouter()
router.register(r'vehiculos', VehiculoAdminViewSet, basename='vehiculos-admin')

urlpatterns = [
    path('', include(router.urls)),
]
