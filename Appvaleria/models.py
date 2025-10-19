from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models


class Paciente(models.Model):
    id_paciente = models.BigAutoField(primary_key=True)
    rut = models.CharField(max_length=15, unique=True, verbose_name="RUT")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    apellido = models.CharField(max_length=50, verbose_name="Apellido")
    email = models.EmailField(max_length=100, verbose_name="Correo electrónico")
    direccion = models.CharField(max_length=150, verbose_name="Dirección")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    prevision = models.CharField(max_length=100, verbose_name="Previsión")
    usuarios_id_usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Usuario asociado',
        db_column='usuarios_id_usuario'  # <- Esto evita que Django agregue _id
    )

    class Meta:
        db_table = 'pacientes'
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"





class FichaMedica(models.Model):
    id_ficha = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=120)
    notas = models.TextField(blank=True, null=True)
    hora_ficha = models.DateTimeField(blank=True, null=True)
    direccion_paciente = models.CharField(max_length=100, blank=True, null=True)
    telefono_paciente = models.CharField(max_length=15, blank=True, null=True)
    rut_paciente = models.CharField(max_length=15, blank=True, null=True)
    nombre_paciente = models.CharField(max_length=50, blank=True, null=True)
    apellido_paciente = models.CharField(max_length=50, blank=True, null=True)
    prevision_paciente = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'ficha_medica'

    def __str__(self):
        return f"Ficha de {self.nombre_paciente}"