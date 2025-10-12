from django.db import models

# Modelo para guardar las horas agendadas
class HoraAgendada(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_final = models.TimeField()
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
