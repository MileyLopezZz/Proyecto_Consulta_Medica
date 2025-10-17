from django.shortcuts import render, redirect
from .models import HoraAgendada
from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages

def agendar_hora_view(request):
    # Verificar si el usuario está logueado 
    if not request.session.get('usuario_id'):
        messages.error(request, "Debes iniciar sesión para agendar una hora.")
        return redirect('login')  # nombre de la vista de login en tus urls.py

    # Simular horarios disponibles
    horarios_disponibles = {
        'Lunes a Jueves': [('10:30 AM', '01:00 PM'), ('03:00 PM', '07:00 PM')],
        'Viernes': [('10:30 AM', '01:00 PM')],
    }

    # Procesar formulario si envía un POST
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        if fecha and hora:
            messages.success(request, f"Hora agendada para {fecha} a las {hora} correctamente.")
            return redirect('confirmacionHora')
        else:
            messages.error(request, "Por favor, selecciona fecha y hora.")

    return render(request, 'Appclaudio/agendarHora.html', {'horarios_disponibles': horarios_disponibles})


def confirmacion_view(request):
    return render(request, 'Appclaudio/confirmacion.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Secretaria
from .forms import SecretariaForm

# --- CRUD Secretaria ---

def listar_secretarias(request):
    secretarias = Secretaria.objects.all()
    return render(request, 'Appclaudio/listar_secretarias.html', {'secretarias': secretarias})

def crear_secretaria(request):
    if request.method == 'POST':
        form = SecretariaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Secretaria agregada correctamente.")
            return redirect('listar_secretarias')
    else:
        form = SecretariaForm()
    return render(request, 'Appclaudio/form_secretaria.html', {'form': form, 'titulo': 'Agregar Secretaria'})

def editar_secretaria(request, pk):
    secretaria = get_object_or_404(Secretaria, pk=pk)
    if request.method == 'POST':
        form = SecretariaForm(request.POST, instance=secretaria)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente.")
            return redirect('listar_secretarias')
    else:
        form = SecretariaForm(instance=secretaria)
    return render(request, 'Appclaudio/form_secretaria.html', {'form': form, 'titulo': 'Editar Secretaria'})

def eliminar_secretaria(request, pk):
    secretaria = get_object_or_404(Secretaria, pk=pk)
    if request.method == 'POST':
        secretaria.delete()
        messages.success(request, "Secretaria eliminada correctamente.")
        return redirect('listar_secretarias')
    return render(request, 'Appclaudio/eliminar_secretaria.html', {'secretaria': secretaria})
