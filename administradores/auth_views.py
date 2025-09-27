# administradores/auth_views.py
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .auth_serializers import CustomTokenObtainPairSerializer

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token_str = request.data.get("refresh")
        if not token_str:
            return Response({"detail": "refresh token requerido"}, status=400)
        try:
            RefreshToken(token_str).blacklist()
        except Exception:
            return Response({"detail": "refresh inválido"}, status=400)
        return Response(status=status.HTTP_205_RESET_CONTENT)

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        u = request.user
        return Response({
            "id": u.id,
            "username": u.usuario,     
            "first_name": u.nombres,
            "last_name": u.apellido,
            "email": u.email or "",
        })
