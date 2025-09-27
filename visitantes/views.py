# visitantes/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from .models import Visitante
from .serializers import VisitanteSerializer


class PublicVisitanteViewSet(viewsets.ModelViewSet):
    """
    CRUD público para la app móvil.
    /api/mobile/visitantes/...
    """
    queryset = Visitante.objects.all().order_by("-created_at")
    serializer_class = VisitanteSerializer
    permission_classes = [permissions.AllowAny]   # público

    def get_queryset(self):
        qs = super().get_queryset()
        cop_id = self.request.query_params.get("copropietario")
        if cop_id:
            qs = qs.filter(copropietario_id=cop_id)
        return qs

    @action(detail=False, methods=["GET"], url_path="por-fecha", permission_classes=[permissions.AllowAny])
    def por_fecha(self, request):
        """
        GET /api/mobile/visitantes/por-fecha/?fecha=YYYY-MM-DD
        Filtra visitantes por fechaIngreso exacta.
        """
        fecha = request.query_params.get("fecha")
        if not fecha:
            return Response({"detail": "Parámetro 'fecha' es requerido (YYYY-MM-DD)."}, status=400)

        f = parse_date(fecha)
        if not f:
            return Response({"detail": "Formato de 'fecha' inválido (usa YYYY-MM-DD)."}, status=400)

        qs = self.get_queryset().filter(fechaIngreso=f)

        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)

        ser = self.get_serializer(qs, many=True)
        return Response(ser.data, status=200)

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny], url_path="verificar")
    def verificar(self, request, pk=None):
        """
        POST /api/mobile/visitantes/{id}/verificar/
        Body: { "foto_b64": "<base64>" }
        Por ahora solo valida que venga la foto. La comparación se implementará después.
        """
        _ = self.get_object()
        foto_b64 = (request.data.get("foto_b64") or "").strip()
        if not foto_b64:
            return Response({"detail": "foto_b64 es requerida"}, status=400)

        # TODO: aquí haremos la comparación con foto1_b64 y foto2_b64 del visitante.
        # match_score_1 = comparar(foto_b64, obj.foto1_b64)
        # match_score_2 = comparar(foto_b64, obj.foto2_b64)
        # return Response({"ok": max(match_score_1,match_score_2) >= 0.8})

        return Response({"status": "pendiente", "message": "Comparación aún no implementada"}, status=200)
