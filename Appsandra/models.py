from django.db import models
from django.utils import timezone

# Create your models here.

#Se crea la tabla de usuarios en la base de datos
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    fecha_signup = models.DateTimeField(default=timezone.now)   #Fecha de registro