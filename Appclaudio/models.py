from django.db import models
from django.core.exceptions import ValidationError
from datetime import time
from django.conf import settings
from django.core.validators import RegexValidator

# Modelo para guardar las horas agendadas
class HoraAgendada(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_final = models.TimeField()
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE,related_name='horas_agendadas',null=True,blank=True)
    razon = models.CharField(max_length=300)
    estado = models.CharField(
        max_length=20, 
        choices=[
            ('Pendiente', 'Pendiente'), 
            ('Confirmada', 'Confirmada'), 
            ('Cancelada', 'Cancelada')
        ],
        default='Pendiente')
    def clean(self):
        rangos = [(time(10, 30), time(13, 0))]              # siempre
        if self.fecha.weekday() in (0, 1, 2, 3):             # lun–jue
            rangos.append((time(15, 0), time(19, 0)))

        if not any(r0 <= self.hora_inicio < self.hora_final <= r1 for r0, r1 in rangos):
            raise ValidationError("La hora está fuera del horario de atención.")

        super().clean()


class Secretaria(models.Model):
    id_secretaria = models.BigAutoField(
        primary_key=True,
        db_column='id_secretaria'
    )

    # validaddores
    rut_validator = RegexValidator(
        # 12.345.678-9  o  12345678-9
        regex=r'^(\d{1,2}\.\d{3}\.\d{3}-[\dkK]|\d{7,8}-[\dkK])$',
        message='Ingrese un RUT válido, ej: 12.345.678-9 o 12345678-9.'
    )

    nombre_validator = RegexValidator(
        regex=r'^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$',
        message='El nombre solo puede contener letras y espacios.'
    )

    apellido_validator = RegexValidator(
        regex=r'^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$',
        message='El apellido solo puede contener letras y espacios.'
    )


    # campos
    rut_secretaria = models.CharField(
        max_length=15,
        unique=True,
        validators=[rut_validator],
        db_column='rut_secretaria'
    )
    nombre_secretaria = models.CharField(
        max_length=50,
        validators=[nombre_validator],
        db_column='nombre_secretaria'
    )
    apellido_secretaria = models.CharField(
        max_length=50,
        validators=[apellido_validator],
        db_column='apellido_secretaria'
    )
    email_secretaria = models.EmailField(
        max_length=100,
        unique=True,
        db_column='email_secretaria'
    )
    password_hash = models.CharField(
        max_length=255,
        db_column='password_hash'
    )
    usuarios_id_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='usuarios_id_usuario',
        related_name='secretarias'
    )

    class Meta:
        db_table = 'secretaria'
        managed = False   

    def __str__(self):
        return f"{self.nombre_secretaria} {self.apellido_secretaria}"

    # Validaciones extra a nivel de objeto
    def clean(self):
        super().clean()

        #normalizar strings
        if self.nombre_secretaria:
            self.nombre_secretaria = self.nombre_secretaria.strip().title()
        if self.apellido_secretaria:
            self.apellido_secretaria = self.apellido_secretaria.strip().title()

        #evitar que nombre y apellido sean muy cortos
        if len(self.nombre_secretaria) < 2:
            raise ValidationError({'nombre_secretaria': 'El nombre es demasiado corto.'})
        if len(self.apellido_secretaria) < 2:
            raise ValidationError({'apellido_secretaria': 'El apellido es demasiado corto.'})
