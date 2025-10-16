from django.db import models
from django.core.exceptions import ValidationError
from datetime import time

# Modelo para guardar las horas agendadas
class HoraAgendada(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_final = models.TimeField()
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    razon = models.CharField(max_length=300)

    def clean(self):
        rangos = [(time(10, 30), time(13, 0))]              # siempre
        if self.fecha.weekday() in (0, 1, 2, 3):             # lun–jue
            rangos.append((time(15, 0), time(19, 0)))

        if not any(r0 <= self.hora_inicio < self.hora_final <= r1 for r0, r1 in rangos):
            raise ValidationError("La hora está fuera del horario de atención.")

        super().clean()