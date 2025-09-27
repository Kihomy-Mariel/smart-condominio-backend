from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Copropietario
from .serializers import CopropietarioSerializer

class CopropietarioViewSet(viewsets.ModelViewSet):
    queryset = Copropietario.objects.all().order_by("apellido", "nombre")
    serializer_class = CopropietarioSerializer
    # 🔐 solo admins (JWT de admin con is_staff=True)
    permission_classes = [permissions.IsAdminUser]

