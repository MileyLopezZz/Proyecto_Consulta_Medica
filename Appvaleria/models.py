from django.db import models

class Paciente(models.Model):
    id_paciente = models.BigAutoField(primary_key=True)
    rut = models.CharField(max_length=15, unique=True, verbose_name="RUT", blank=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre", blank=True)
    apellido = models.CharField(max_length=50, verbose_name="Apellido", blank=True)
    email = models.EmailField(max_length=100, verbose_name="Correo electrónico", blank=True)
    direccion = models.CharField(max_length=150, verbose_name="Dirección", blank=True)
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", blank=True)
    prevision = models.CharField(max_length=100, verbose_name="Previsión", blank=True)
    usuarios_id_usuario = models.IntegerField(null=True, blank=True, verbose_name="ID del usuario (opcional)")

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