from django import forms
from .models import Usuario
from django.contrib.auth.hashers import make_password , check_password   # importacion para poder encriptar/ verfificar contrasenias


class RegistroForm(forms.ModelForm):
    # Campos adicionales agregados que no existen directamente en el modelo
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    confirmar_password = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    #Esta clase meta indica a que modelo esta asociado y que campos debe mostrar
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'password'] 

    # Validación personalizada
    def clean(self):
        # ejecuta todas las validaciones individuales de cada campo
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        # Si las contraseñas no coinciden, se lanza un error de validación
        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    # Guardar el usuario
    def save(self, commit=True):
        usuario = super().save(commit=False)
        #Encriptamos la contraseña antes de guardarla en la base de datos
        usuario.password_hash = make_password(self.cleaned_data['password'])
        if commit:
            usuario.save()  # Se inserta en la BD
        return usuario


# Formulario de login
class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)