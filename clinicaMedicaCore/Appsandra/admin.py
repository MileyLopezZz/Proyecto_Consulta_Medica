from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Usuario

# ✅ Registrar el modelo Usuario en el admin
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'email', 'fecha_signup')  
    search_fields = ('nombre', 'apellido', 'email')                      
    list_filter = ('fecha_signup',)     