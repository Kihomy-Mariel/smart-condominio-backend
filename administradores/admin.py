# administradores/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Administrador

@admin.register(Administrador)
class AdministradorAdmin(UserAdmin):
    model = Administrador
    list_display = ("id", "usuario", "apellido", "nombres", "carnet", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("usuario", "apellido", "nombres", "carnet", "email")
    ordering = ("apellido", "nombres")

    fieldsets = (
        (None, {"fields": ("usuario", "password")}),
        ("Datos personales", {"fields": ("nombres", "apellido", "carnet", "telefono", "direccion", "email")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("nombres", "apellido", "carnet", "usuario", "password1", "password2", "is_staff", "is_active"),
        }),
    )
