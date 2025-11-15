from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import HoraAgendadaForm

def agendar_hora_view(request):
    # Validar sesión 
    if not request.user.is_autenthicated:
        messages.error(request, "Debes iniciar sesión para agendar una hora.")
        return redirect('login')

    # Si se envía una fecha, calculamos los horarios disponibles
    if request.method == 'POST':
        form = HoraAgendadaForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.usuario = request.user

            dt_inicio=datetime.combine(instancia.fecha, instancia.hora_inicio)
            instancia.hora_final = (dt_inicio + timedelta(minutes=30)).time()

            instancia.save()
            messages.success(request, "Hora agendada con éxito.")
            return redirect('confirmacion')

    else:
        form = HoraAgendadaForm(initial={'estado' : 'Pendiente'})

    return render(request, 'Appclaudio/agendarHora.html', {
        'form': form,
    })

def confirmacion_view(request):
    return render(request, 'Appclaudio/confirmacion.html')


# --- CRUD Secretaria ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Secretaria
from .forms import SecretariaForm



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
