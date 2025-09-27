from django.db import models
from django.contrib.auth.hashers import make_password
import re

class Guardia(models.Model):
    class Turno(models.TextChoices):
        DIA = "DIA", "Día"
        NOCHE = "NOCHE", "Noche"
        ROTATIVO = "ROTATIVO", "Rotativo"

    nombre     = models.CharField(max_length=120)
    apellido   = models.CharField(max_length=120)
    carnet     = models.CharField(max_length=20, unique=True)
    correo     = models.EmailField(unique=True)
    telefono   = models.CharField(max_length=30, blank=True)

    usuario    = models.CharField(max_length=150, unique=True, editable=False)
    contrasena = models.CharField(max_length=128)  # hash Django

    turno      = models.CharField(max_length=10, choices=Turno.choices, default=Turno.ROTATIVO)
    empresa    = models.CharField(max_length=120, blank=True)
    puesto     = models.CharField(max_length=120, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "guardia"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.usuario})"

    def save(self, *args, **kwargs):
        # usuario = inicial apellido + solo dígitos del carnet
        if not self.usuario and self.apellido and self.carnet:
            inicial = (self.apellido.strip()[0].lower() if self.apellido and self.apellido.strip() else "x")
            solo_digitos = re.sub(r"\D", "", str(self.carnet))
            self.usuario = f"{inicial}{solo_digitos}"

        # si la contraseña no parece hash, hasheamos
        if self.contrasena and not self.contrasena.startswith(("pbkdf2_", "argon2")):
            self.contrasena = make_password(self.contrasena)

        super().save(*args, **kwargs)
