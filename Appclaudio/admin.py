from django.contrib import admin
from .models import Secretaria

@admin.register(Secretaria)
class SecretariaAdmin(admin.ModelAdmin):
    # columnas que se ven en la tabla
    list_display = (
        'id_secretaria',
        'rut_secretaria',
        'nombre_secretaria',
        'apellido_secretaria',
        'email_secretaria',
        'usuarios_id_usuario',  
    )

    # barra de búsqueda
    search_fields = (
        'rut_secretaria',
        'nombre_secretaria',
        'apellido_secretaria',
        'email_secretaria',
    )

    # filtros laterales
    list_filter = ('usuarios_id_usuario',)

    # orden por defecto
    ordering = ('apellido_secretaria', 'nombre_secretaria')
