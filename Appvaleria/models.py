from django.db import models

class Paciente(models.Model):
    id_paciente = models.BigAutoField(primary_key=True)
    rut = models.CharField(max_length=15)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=15)
    prevision = models.CharField(max_length=100)
    usuarios_id_usuario = models.BigIntegerField()

    class Meta:
        db_table = 'pacientes'  # ← usa la tabla real de MySQL


class FichaMedica(models.Model):
    id_ficha = models.BigAutoField(primary_key=True)
    # paciente = models.ForeignKey(
    #     Paciente, on_delete=models.CASCADE, null=True, blank=True
    # ) SE USARA PARA LA SIGUIENTE ENTREGA
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
        db_table = 'ficha_medica'  # ← aquí el nombre correcto

    def __str__(self):
        return f"Ficha de {self.nombre_paciente}"
