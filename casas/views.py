from django.shortcuts import render

from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Casa
from .serializers import CasaSerializer


# ========= ADMIN (CRUD completo, protegido) =========
class CasaAdminViewSet(viewsets.ModelViewSet):
    queryset = Casa.objects.all().select_related('copropietario')
    serializer_class = CasaSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    # POST /api/casas/admin/crear-casa
    @action(detail=False, methods=['post'], url_path='admin/crear-casa')
    def crear_casa(self, request):
        data = dict(request.data)
        data['tipo'] = 'CASA'
        if data.get('piso') in ('', None):
            data['piso'] = None
        ser = self.serializer_class(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)

    # POST /api/casas/admin/crear-departamento
    @action(detail=False, methods=['post'], url_path='admin/crear-departamento')
    def crear_departamento(self, request):
        data = dict(request.data)
        data['tipo'] = 'DEPARTAMENTO'
        ser = self.serializer_class(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


# ========= MÓVIL (listados libres) =========
class CasaMobileViewSet(viewsets.GenericViewSet):
    queryset = Casa.objects.all().select_related('copropietario')
    serializer_class = CasaSerializer
    permission_classes = [permissions.AllowAny]

    # GET /api/mobile/casas/casas?copropietario_id=#
    @action(detail=False, methods=['get'], url_path='casas')
    def listar_casas(self, request):
        cop_id = request.query_params.get('copropietario_id')
        if not cop_id:
            return Response({'detail': 'copropietario_id es requerido.'},
                            status=status.HTTP_400_BAD_REQUEST)
        qs = self.get_queryset().filter(
            tipo='CASA', copropietario_id=cop_id
        ).order_by('bloque', 'torre', 'numero')
        return Response(self.serializer_class(qs, many=True).data)

    # GET /api/mobile/casas/departamentos?copropietario_id=#
    @action(detail=False, methods=['get'], url_path='departamentos')
    def listar_departamentos(self, request):
        cop_id = request.query_params.get('copropietario_id')
        if not cop_id:
            return Response({'detail': 'copropietario_id es requerido.'},
                            status=status.HTTP_400_BAD_REQUEST)
        qs = self.get_queryset().filter(
            tipo='DEPARTAMENTO', copropietario_id=cop_id
        ).order_by('torre', 'piso', 'numero')
        return Response(self.serializer_class(qs, many=True).data)

