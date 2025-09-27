from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Guardia

class GuardiaSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Guardia
        fields = [
            "id", "nombre", "apellido", "carnet", "correo", "telefono",
            "usuario", "turno", "empresa", "puesto", "new_password",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "usuario", "created_at", "updated_at"]

    def create(self, validated_data):
        raw = validated_data.pop("new_password", "").strip()
        obj = Guardia(**validated_data)
        # contraseña por defecto: carnet (hasheará en save)
        obj.contrasena = raw if raw else obj.carnet
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
