from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta, timezone as dt_tz
import jwt
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Copropietario

SECRET = getattr(settings, "COPROPIETARIO_JWT_SECRET", settings.SECRET_KEY)
LIFETIME = getattr(settings, "COPROPIETARIO_ACCESS_LIFETIME", timedelta(days=7))

def build_token(payload: dict) -> str:
    now = datetime.now(dt_tz.utc)
    body = {
        "iss": "backend_condominio",
        "aud": "copropietario",
        "iat": int(now.timestamp()),
        "exp": int((now + LIFETIME).timestamp()),
        **payload,
    }
    return jwt.encode(body, SECRET, algorithm="HS256")

class LoginCopropietarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        usuario = (request.data.get("usuario") or "").strip()
        password = (request.data.get("password") or "").strip()
        if not usuario or not password:
            return Response({"detail": "usuario y password requeridos"}, status=400)

        try:
            cop = Copropietario.objects.get(usuario=usuario)
        except Copropietario.DoesNotExist:
            return Response({"detail": "Credenciales incorrectas"}, status=400)

        if not check_password(password, cop.contrasena):
            return Response({"detail": "Credenciales incorrectas"}, status=400)

        token = build_token({
            "scope": "copropietario",
            "sub": f"cop:{cop.id}",
            "copropietario_id": cop.id,
            "usuario": cop.usuario,
            "nombre": cop.nombre,
            "apellido": cop.apellido,
            "carnet": cop.carnet,
            "correo": cop.correo,
        })

        return Response({
            "token": token,
            "copropietario": {
                "id": cop.id,
                "usuario": cop.usuario,
                "nombre": cop.nombre,
                "apellido": cop.apellido,
                "carnet": cop.carnet,
                "correo": cop.correo,
            }
        }, status=200)

class LogoutCopropietarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Con JWT stateless “móvil” no hay server-side logout por defecto.
        # El cliente debe descartar el token. (Podemos añadir blacklist luego)
        return Response(status=status.HTTP_205_RESET_CONTENT)
