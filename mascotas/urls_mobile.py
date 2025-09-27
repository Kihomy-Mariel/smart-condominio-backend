from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MascotaMobileViewSet

router = DefaultRouter()
router.register(r'mobile/mascotas', MascotaMobileViewSet, basename='mascotas-mobile')

urlpatterns = [
    path('', include(router.urls)),
]
