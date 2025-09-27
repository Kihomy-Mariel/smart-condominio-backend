from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CasaMobileViewSet

router = DefaultRouter()
router.register(r'mobile/casas', CasaMobileViewSet, basename='casas-mobile')

urlpatterns = [
    path('', include(router.urls)),
]
