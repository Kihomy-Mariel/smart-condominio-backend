from django.db import models

class Visitante(models.Model):
    class Estado(models.IntegerChoices):
        PENDIENTE = 0, "pendiente"
        INGRESO   = 1, "ingreso"
        SALIO     = 2, "salio"

    nombre        = models.CharField(max_length=120)

    fechaIngreso  = models.DateField()
    fechaSalida   = models.DateField(null=True, blank=True)

    horaIngreso   = models.TimeField()
    horaSalida    = models.TimeField(null=True, blank=True)

    placa         = models.CharField(max_length=20, blank=True)

    estado        = models.PositiveSmallIntegerField(
        choices=Estado.choices, default=Estado.PENDIENTE
    )

    # Guardamos base64 como texto (luego podemos migrar a archivos/URLs)
    foto1_b64     = models.TextField()
    foto2_b64     = models.TextField()

    # FK al modelo de la otra app
    copropietario = models.ForeignKey(
        "copropietarios.Copropietario",   # <- referencia por string para evitar import circular
        on_delete=models.CASCADE,
        related_name="visitantes"
    )

    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "visitante"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"
