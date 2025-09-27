from django.db import models
from casas.models import Casa  # FK a la unidad

class Vehiculo(models.Model):
    id = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=20)
    marca = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE, related_name='vehiculos')

    class Meta:
        db_table = 'vehiculo'
        indexes = [
            models.Index(fields=['placa']),
            models.Index(fields=['casa']),
        ]
        # si deseas evitar duplicados de placa dentro de la misma casa:
        constraints = [
            models.UniqueConstraint(fields=['placa', 'casa'], name='uq_placa_por_casa')
        ]

    def __str__(self):
        return f'{self.placa} ({self.marca or ""})'
