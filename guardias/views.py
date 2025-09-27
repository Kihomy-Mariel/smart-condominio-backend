from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Guardia
from .serializers import GuardiaSerializer

class GuardiaViewSet(viewsets.ModelViewSet):
    queryset = Guardia.objects.all().order_by("apellido", "nombre")
    serializer_class = GuardiaSerializer
    # 🔐 solo accesible con JWT de administrador (is_staff=True)
    permission_classes = [permissions.IsAdminUser]
