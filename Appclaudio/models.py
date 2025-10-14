from django.db import models

# Modelo para guardar las horas agendadas
class HoraAgendada(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField(default = "08:00:00")
    hora_final = models.TimeField(default = "09:00:00")
    razon = models.CharField(max_length=300)
