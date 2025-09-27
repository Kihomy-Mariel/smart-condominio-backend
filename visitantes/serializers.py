from rest_framework import serializers
from .models import Visitante
import base64

class VisitanteSerializer(serializers.ModelSerializer):
    estado_texto = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Visitante
        fields = [
            "id",
            "nombre",
            "fechaIngreso",
            "fechaSalida",
            "horaIngreso",
            "horaSalida",
            "placa",
            "estado",        # 0/1/2
            "estado_texto",
            "foto1_b64",
            "foto2_b64",
            "copropietario",
            "created_at",
            "updated_at",
        ]
    def get_estado_texto(self, obj):
        return obj.get_estado_display()

    def validate(self, attrs):
        f_in = attrs.get("fechaIngreso", getattr(self.instance, "fechaIngreso", None))
        f_out = attrs.get("fechaSalida", getattr(self.instance, "fechaSalida", None))
        h_in = attrs.get("horaIngreso", getattr(self.instance, "horaIngreso", None))
        h_out = attrs.get("horaSalida", getattr(self.instance, "horaSalida", None))

        if f_out and f_in and f_out < f_in:
            raise serializers.ValidationError("fechaSalida no puede ser menor a fechaIngreso.")
        if f_out == f_in and h_out and h_in and h_out < h_in:
            raise serializers.ValidationError("horaSalida no puede ser menor a horaIngreso cuando la fecha es la misma.")

        for key in ("foto1_b64", "foto2_b64"):
            b64 = attrs.get(key, getattr(self.instance, key, None))
            if b64:
                try:
                    if "," in b64:
                        b64 = b64.split(",", 1)[1]
                    base64.b64decode(b64, validate=True)
                except Exception:
                    raise serializers.ValidationError({key: "Imagen base64 inválida."})
        return attrs
