from django.db import models

from django.db import models
from copropietarios.models import Copropietario   # relación con el dueño principal

class Casa(models.Model):
    TIPO_CHOICES = (
        ('CASA', 'CASA'),
        ('DEPARTAMENTO', 'DEPARTAMENTO'),
    )

    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=50)                  # número de casa o dpto
    piso = models.IntegerField(null=True, blank=True)         # obligatorio solo para depto
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    torre = models.CharField(max_length=100, null=True, blank=True)
    bloque = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    area_m2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    copropietario = models.ForeignKey(
        Copropietario,
        on_delete=models.CASCADE,
        related_name='unidades'
    )

    class Meta:
        db_table = 'casa'
        constraints = [
            models.UniqueConstraint(
                fields=['tipo', 'torre', 'bloque', 'piso', 'numero', 'copropietario'],
                name='uq_unidad_por_propietario_y_ubicacion'
            )
        ]

    def __str__(self):
        return f'{self.tipo} {self.numero} (coprop: {self.copropietario_id})'

