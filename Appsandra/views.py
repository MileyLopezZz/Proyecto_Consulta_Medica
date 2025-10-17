from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario
from . forms import RegistroForm,LoginForm

# Create your views here.

def RegisterUser(request):
    if request.method == 'POST' :
        form = RegistroForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registro Exitoso ✅")
            return redirect('login')
    else:
        form = RegistroForm()
            
    return render(request, 'Registro.html', {'form' : form})



def loginUser(request):
    if request.method == 'POST' :
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                usuario = Usuario.objects.get(email=email)  #busca el usuario por correo
                if check_password(password, usuario.password_hash):
                    #guarda los datos ensesion (se crea una cookie de sesion)
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_nombre'] = usuario.nombre
                    messages.success(request,"Inicio sesión con exito")
                    return redirect('UsuarioView') # redirije a la vista de usuario.
                else:
                    messages.error(request, "Contraseña incorrecta ❌")
            except Usuario.DoesNotExist:
                messages.error(request, "El usuario es Incorrecto ❌")
    else:
        form = LoginForm()

    
    return render(request, 'Login.html', {'form' : form})



"""def UserView(request):
    return render(request, 'UserView.html')"""

def UserView(request):
    #Recuperar el ID del usuario desde la sesión
    usuario_id = request.session.get('usuario_id')

    # 3️⃣ Buscar al usuario en la base de datos
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe ❌")
        return redirect('login')

    # 4️⃣ Pasar el usuario al template
    data = {
        'usuario': usuario
    }

    return render(request, 'UserView.html', data)
