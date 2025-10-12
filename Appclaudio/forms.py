from django import forms
from .models import HoraAgendada
from datetime import date

class HoraAgendadaForm(forms.ModelForm):
    class Meta:
        model = HoraAgendada
        fields = ['fecha', 'hora_inicio', 'razon', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'razon': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado': forms.HiddenInput(),  # Estado es oculto, se asignará por defecto
        }

    # Validaciones personalizadas
    def clean_hora_inicio(self):
        fecha = self.cleaned_data['fecha']
        hora = self.cleaned_data['hora_inicio']

        # Validación: Horarios permitidos
        if not self.is_valid_hora(fecha, hora):
            raise forms.ValidationError("La hora seleccionada no está disponible.")
        return hora

    def is_valid_hora(self, fecha, hora):
        # Definir los horarios por días
        horarios_permitidos = {
            0: [('10:30', '13:00'), ('15:00', '19:00')],  # Lunes
            1: [('10:30', '13:00'), ('15:00', '19:00')],  # Martes
            2: [('10:30', '13:00'), ('15:00', '19:00')],  # Miércoles
            3: [('10:30', '13:00'), ('15:00', '19:00')],  # Jueves
            4: [('10:30', '13:00')],  # Viernes
        }

        # Obtener el día de la semana (0=domingo, 1=lunes, ..., 6=sábado)
        dia_semana = fecha.weekday()

        # Validar si la hora seleccionada está dentro de los horarios permitidos
        for rango in horarios_permitidos.get(dia_semana, []):
            if rango[0] <= hora <= rango[1]:
                return True
        return False
