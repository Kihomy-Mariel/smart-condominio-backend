# administradores/views.py
from rest_framework import viewsets, permissions
from .models import Administrador
from .serializers import AdministradorSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all().order_by("apellido", "nombres")
    serializer_class = AdministradorSerializer
    permission_classes = [permissions.IsAuthenticated]
