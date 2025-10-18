from django import forms
from .models import FichaMedica, Paciente


class FichaMedicaForm(forms.ModelForm):
    rut_paciente = forms.CharField(
        label='RUT Paciente',
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese RUT del paciente',
            'class': 'form-control'
        })
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
            'nombre_paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Ej: Diagnóstico de Gripe',
                'class': 'form-control'
            }),
            'notas': forms.Textarea(attrs={
                'placeholder': 'Escriba aquí las observaciones médicas...',
                'class': 'form-control'
            }),
            'hora_ficha': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'rut', 'nombre', 'apellido', 'email', 'direccion', 'telefono', 'prevision'
        ]
        labels = {
            'rut': 'RUT Paciente',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'email': 'Correo electrónico',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'prevision': 'Previsión',
        }
        widgets = {
            'rut': forms.TextInput(attrs={'placeholder': 'Ingrese RUT', 'class': 'form-control', 'required': False}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese nombre', 'class': 'form-control', 'required': False}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese apellido', 'class': 'form-control', 'required': False}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese correo', 'class': 'form-control', 'required': False}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Ingrese dirección', 'class': 'form-control', 'required': False}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese teléfono', 'class': 'form-control', 'required': False}),
            'prevision': forms.TextInput(attrs={'placeholder': 'Ej: Fonasa, Isapre...', 'class': 'form-control', 'required': False}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if Paciente.objects.filter(rut=rut).exclude(id_paciente=self.instance.id_paciente).exists():
            raise forms.ValidationError("Ya existe un paciente con este RUT.")
        return rut

