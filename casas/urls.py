from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CasaAdminViewSet

router = DefaultRouter()
router.register(r'casas', CasaAdminViewSet, basename='casas-admin')

urlpatterns = [
    path('', include(router.urls)),
]
