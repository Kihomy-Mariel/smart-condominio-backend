from django.conf import settings
from datetime import datetime, timedelta, timezone as dt_tz
import jwt
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Guardia

SECRET = getattr(settings, "COPROPIETARIO_JWT_SECRET", settings.SECRET_KEY)
LIFETIME = getattr(settings, "COPROPIETARIO_ACCESS_LIFETIME", timedelta(days=7))

def build_token(payload: dict) -> str:
    now = datetime.now(dt_tz.utc)
    body = {
        "iss": "backend_condominio",
        "aud": "guardia",
        "iat": int(now.timestamp()),
        "exp": int((now + LIFETIME).timestamp()),
        **payload,
    }
    return jwt.encode(body, SECRET, algorithm="HS256")

class LoginGuardiaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        usuario = (request.data.get("usuario") or "").strip()
        password = (request.data.get("password") or "").strip()
        if not usuario or not password:
            return Response({"detail": "usuario y password requeridos"}, status=400)

        try:
            guardia = Guardia.objects.get(usuario=usuario)
        except Guardia.DoesNotExist:
            return Response({"detail": "Credenciales incorrectas"}, status=400)

        if not check_password(password, guardia.contrasena):
            return Response({"detail": "Credenciales incorrectas"}, status=400)

        token = build_token({
            "scope": "guardia",
            "sub": f"guard:{guardia.id}",
            "guardia_id": guardia.id,
            "usuario": guardia.usuario,
            "nombre": guardia.nombre,
            "apellido": guardia.apellido,
            "carnet": guardia.carnet,
            "correo": guardia.correo,
            "telefono": guardia.telefono,
            "turno": guardia.turno,
            "empresa": guardia.empresa,
            "puesto": guardia.puesto,
        })

        return Response({
            "token": token,
            "guardia": {
                "id": guardia.id,
                "usuario": guardia.usuario,
                "nombre": guardia.nombre,
                "apellido": guardia.apellido,
                "carnet": guardia.carnet,
                "correo": guardia.correo,
                "telefono": guardia.telefono,
                "turno": guardia.turno,
                "empresa": guardia.empresa,
                "puesto": guardia.puesto,
            }
        }, status=200)

class LogoutGuardiaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Stateless: el cliente (app móvil) debe descartar el token localmente
        return Response({"detail": "Token descartado en cliente"}, status=status.HTTP_205_RESET_CONTENT)
