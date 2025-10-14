from django import forms
from .models import FichaMedica  

class FichaMedicaForm(forms.ModelForm):
    rut_paciente = forms.CharField(
        label='RUT Cliente',
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese RUT del cliente'})
    )

    class Meta:
        model = FichaMedica
        fields = [
            'rut_paciente',      
            'nombre_paciente',
            'telefono_paciente',
            'direccion_paciente',
            'titulo',
            'notas',
            'hora_ficha',
        ]
        widgets = {
            'notas': forms.Textarea(attrs={'placeholder': 'Escriba aquí las observaciones médicas...'}),
            'titulo': forms.TextInput(attrs={'placeholder': 'Ej: Diagnóstico de Gripe'}),
            'hora_ficha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
}



