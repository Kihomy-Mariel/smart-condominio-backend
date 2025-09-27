from rest_framework import serializers
from .models import Mascota

class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'raza', 'color', 'foto', 'casa']

    def validate_nombre(self, value):
        v = (value or '').strip()
        if not v:
            raise serializers.ValidationError('El nombre es obligatorio.')
        return v

    def validate_foto(self, value):
        # opcional, si viene, debe parecer base64
        if value in (None, '',):
            return value
        if isinstance(value, str) and all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n\r' for c in value.strip()):
            return value.strip()
        raise serializers.ValidationError('La foto debe ser una cadena en base64.')
