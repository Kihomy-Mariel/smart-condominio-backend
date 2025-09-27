from rest_framework import serializers
from .models import Vehiculo

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['id', 'placa', 'marca', 'color', 'descripcion', 'casa']

    def validate_placa(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('La placa es obligatoria.')
        return value.strip().upper()
