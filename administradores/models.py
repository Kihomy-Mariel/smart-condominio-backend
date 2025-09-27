# administradores/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import re

class AdministradorManager(BaseUserManager):
    use_in_migrations = True

    def _build_usuario(self, apellido: str, carnet: str) -> str:
        inicial = (apellido.strip()[0].lower() if apellido and apellido.strip() else "x")
        solo_digitos = re.sub(r"\D", "", str(carnet))
        return f"{inicial}{solo_digitos}"

    # 👇 Acepta 'usuario' opcional y evita duplicado con extra_fields
    def create_user(self, nombres, apellido, carnet, password=None, usuario=None, **extra_fields):
        if not nombres:
            raise ValueError("El campo 'nombres' es obligatorio")
        if not apellido:
            raise ValueError("El campo 'apellido' es obligatorio")
        if not carnet:
            raise ValueError("El campo 'carnet' es obligatorio")

        # Si viene 'usuario' desde createsuperuser, úsalo; si no, genera uno
        if not usuario:
            usuario = self._build_usuario(apellido, carnet)

        # Evita doble asignación si vino en extra_fields
        extra_fields.pop("usuario", None)
        extra_fields.setdefault("is_active", True)

        user = self.model(
            nombres=nombres,
            apellido=apellido,
            carnet=carnet,
            usuario=usuario,
            **extra_fields,
        )
        user.set_password(password or str(carnet))
        user.save(using=self._db)
        return user

    def create_superuser(self, nombres, apellido, carnet, password=None, usuario=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("is_staff=True requerido para superuser")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is_superuser=True requerido para superuser")

        return self.create_user(
            nombres, apellido, carnet,
            password=password,
            usuario=usuario,         # <- pasa usuario si tecleaste uno
            **extra_fields
        )


class Administrador(AbstractBaseUser, PermissionsMixin):
    nombres   = models.CharField(max_length=120)
    apellido  = models.CharField(max_length=120)
    carnet    = models.CharField(max_length=20, unique=True)
    telefono  = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    usuario   = models.CharField(max_length=150, unique=True)  # username
    email     = models.EmailField(blank=True)

    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = AdministradorManager()

    USERNAME_FIELD = "usuario"
    REQUIRED_FIELDS = ["nombres", "apellido", "carnet"]

    class Meta:
        db_table = "administrador"
        ordering = ["apellido", "nombres"]

    def __str__(self):
        return f"{self.usuario} - {self.apellido}, {self.nombres}"

    def save(self, *args, **kwargs):
        # si no hay usuario definido (crear via admin sin usuario), lo derivamos
        if not self.usuario and self.apellido and self.carnet:
            inicial = (self.apellido.strip()[0].lower() if self.apellido and self.apellido.strip() else "x")
            solo_digitos = re.sub(r"\D", "", str(self.carnet))
            self.usuario = f"{inicial}{solo_digitos}"
        super().save(*args, **kwargs)
