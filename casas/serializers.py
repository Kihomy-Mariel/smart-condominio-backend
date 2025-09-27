from rest_framework import serializers
from .models import Casa

class CasaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casa
        fields = [
            'id',
            'numero',
            'piso',
            'tipo',
            'torre',
            'bloque',
            'direccion',
            'area_m2',
            'copropietario'
        ]

    def validate(self, attrs):
        tipo = attrs.get('tipo') or (self.instance.tipo if self.instance else None)
        piso = attrs.get('piso', None)

        # Validación: si es DEPARTAMENTO, el piso es obligatorio
        if tipo == 'DEPARTAMENTO' and piso is None:
            raise serializers.ValidationError({
                'piso': 'Para DEPARTAMENTO el piso es obligatorio.'
            })

        # Validación: si es CASA, el piso debería quedar en null
        if tipo == 'CASA' and piso not in (None, ''):
            raise serializers.ValidationError({
                'piso': 'Para CASA el campo piso debe quedar vacío.'
            })

        return attrs
