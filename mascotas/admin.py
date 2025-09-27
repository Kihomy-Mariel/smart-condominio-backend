from django.contrib import admin
from .models import Mascota

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'raza', 'color', 'casa_id')
    search_fields = ('nombre', 'raza', 'color')
    list_filter = ('raza', 'color')
