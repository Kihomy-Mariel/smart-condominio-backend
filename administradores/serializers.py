# administradores/serializers.py
from rest_framework import serializers
from .models import Administrador

class AdministradorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Administrador
        fields = [
            "id", "nombres", "apellido", "carnet",
            "telefono", "direccion", "usuario", "email",
            "password",
        ]
        read_only_fields = ["id", "usuario"]

    def create(self, validated_data):
        raw_pass = validated_data.pop("password", None)
        # create_user ya se encarga de set_password (usa carnet si no envían password)
        user = Administrador.objects.create_user(password=raw_pass, **validated_data)
        return user

    def update(self, instance, validated_data):
        raw_pass = validated_data.pop("password", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if raw_pass:
            instance.set_password(raw_pass)
            instance.save()
        return instance
