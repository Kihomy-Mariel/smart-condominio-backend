from django.db import models
from casas.models import Casa

class Mascota(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    foto = models.TextField(null=True, blank=True)  # base64 opcional
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE, related_name='mascotas')

    class Meta:
        db_table = 'mascota'
        indexes = [
            models.Index(fields=['casa']),
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return f'{self.nombre} (casa {self.casa_id})'

