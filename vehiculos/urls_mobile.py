from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculoMobileViewSet

router = DefaultRouter()
router.register(r'mobile/vehiculos', VehiculoMobileViewSet, basename='vehiculos-mobile')

urlpatterns = [
    path('', include(router.urls)),
]
