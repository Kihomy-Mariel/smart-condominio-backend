from rest_framework import serializers
from .models import Copropietario
from django.contrib.auth.hashers import make_password

class CopropietarioSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Copropietario
        fields = ["id", "nombre", "apellido", "carnet", "correo", "usuario", "new_password"]
        read_only_fields = ["id", "usuario"]

    def create(self, validated_data):
        raw = validated_data.pop("new_password", "").strip()
        obj = Copropietario(**validated_data)
        obj.contrasena = raw if raw else obj.carnet  # por defecto = carnet
        obj.save()
        return obj

    def update(self, instance, validated_data):
        raw = validated_data.pop("new_password", "").strip()
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if raw:
            instance.contrasena = make_password(raw)
        instance.save()
        return instance
