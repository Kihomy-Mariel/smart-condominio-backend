from django.db import models
from django.contrib.auth.hashers import make_password
import re

class Copropietario(models.Model):
    nombre     = models.CharField(max_length=120)
    apellido   = models.CharField(max_length=120)
    carnet     = models.CharField(max_length=20, unique=True)
    correo     = models.EmailField(unique=True)
    usuario    = models.CharField(max_length=150, unique=True, editable=False)
    contrasena = models.CharField(max_length=128)  

    class Meta:
        db_table = "copropietario"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    def save(self, *args, **kwargs):
        # usuario = inicial apellido (minúscula) + solo dígitos del carnet
        inicial = (self.apellido.strip()[0].lower() if self.apellido and self.apellido.strip() else "x")
        solo_digitos = re.sub(r"\D", "", str(self.carnet))
        self.usuario = f"{inicial}{solo_digitos}"

        # si parece texto plano, hasheamos
        if self.contrasena and not self.contrasena.startswith(("pbkdf2_", "argon2")):
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)
