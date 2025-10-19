from django import forms
from .models import Usuario
from django.contrib.auth.hashers import make_password , check_password   # importacion para poder encriptar/ verfificar contrasenias
import re           #modulo de expresiones regulares


class RegistroForm(forms.ModelForm):
    # Campos adicionales agregados que no existen directamente en el modelo
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'La contraseña es obligatoria'
        })

    
    confirmar_password = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Se debe confirmar la contraseña'
        })


    #Esta clase meta indica a que modelo esta asociado y que campos debe mostrar
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'password'] 

        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Eduardo'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Perez'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Eduardoperez@gmail.com'}),
        }

        error_messages = {
            'nombre': {
                'required': 'El nombre es obligatorio.',
            },
            'apellido': {
                'required': 'El apellido es obligatorio.',
            },
            'email': {
                'required': 'El correo electrónico es obligatorio.',
                'invalid' : 'Ingresa un correo eletronico valido'
            },
            'password': {
                'required': 'La contraseña es obligatoria.',
            }
        }


    #validacion para que se ingrese solamente letras en nombre y apellido
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not nombre.replace(' ', '').isalpha():
            raise forms.ValidationError('Ingresa un Nombre correcto. Solo letras')
        return nombre


    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')

        if not apellido.replace(' ', '').isalpha():
            raise forms.ValidationError('Ingresa un Apellido correcto. Solo letras')
        return apellido


    #validacion de correo existente
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email


    #validacion de contraseña segura
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 CARACTERES")
        
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("La contraseña debe tener al menos una letra MAYÚSCULA")
        
        if not re.search(r'\d', password):
            raise forms.ValidationError('La contraseña debe tener al menos un NÚMERO')
        
        return password
    

    # Validación de comparacion de contrasenias
    def clean(self):
        # ejecuta todas las validaciones individuales de cada campo
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        # Si las contraseñas no coinciden, se lanza un error de validación
        if password and confirmar_password:
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
    email = forms.EmailField(
        label="Correo electrónico",
        error_messages={
            'required': 'El correo es obligatorio',
            'invalid' : 'Ingresa un correo eletronico valido'
        })


    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        error_messages={
            'required': 'La contraseña es obligatoria'
        })