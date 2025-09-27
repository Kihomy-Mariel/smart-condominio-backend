from django.shortcuts import render

from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Mascota
from .serializers import MascotaSerializer

# ======== ADMIN (CRUD completo protegido) ========
class MascotaAdminViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.select_related('casa').all()
    serializer_class = MascotaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

# ======== MÓVIL (público) ========
class MascotaMobileViewSet(viewsets.GenericViewSet):
    queryset = Mascota.objects.select_related('casa').all()
    serializer_class = MascotaSerializer
    permission_classes = [permissions.AllowAny]

    # GET /api/mobile/mascotas/
    def list(self, request):
        qs = self.get_queryset().order_by('nombre')
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.serializer_class(page, many=True)
            return self.get_paginated_response(ser.data)
        return Response(self.serializer_class(qs, many=True).data)

    # GET /api/mobile/mascotas/por-casa/?casa_id=#
    @action(detail=False, methods=['get'], url_path='por-casa')
    def listar_por_casa(self, request):
        casa_id = request.query_params.get('casa_id')
        if not casa_id:
            return Response({'detail': 'casa_id es requerido.'},
                            status=status.HTTP_400_BAD_REQUEST)
        qs = self.get_queryset().filter(casa_id=casa_id).order_by('nombre')
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.serializer_class(page, many=True)
            return self.get_paginated_response(ser.data)
        return Response(self.serializer_class(qs, many=True).data)

