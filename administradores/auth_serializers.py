from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["nombres"]   = user.nombres
        token["apellido"]  = user.apellido
        token["carnet"]    = user.carnet
        token["telefono"]  = user.telefono
        token["direccion"] = user.direccion
        token["usuario"]   = user.usuario
        token["email"]     = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data.update({
            "id": self.user.id,
            "nombres": self.user.nombres,
            "apellido": self.user.apellido,
            "carnet": self.user.carnet,
            "telefono": self.user.telefono,
            "direccion": self.user.direccion,
            "usuario": self.user.usuario,
            "email": self.user.email,
        })
        return data
