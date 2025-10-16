from django.shortcuts import render, redirect
from .models import HoraAgendada
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def agendar_hora_view(request):
    # Definir los horarios disponibles
    lunes_a_jueves = [('10:30 AM', '01:00 PM'), ('03:00 PM', '07:00 PM')]
    viernes = [('10:30 AM', '01:00 PM')]

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')  # Viene en formato "10:30 AM - 01:00 PM"

        if not fecha or not hora:
            messages.error(request, "Por favor selecciona una fecha y hora válida.")
            return redirect('agendar_hora')

        try:
            hora_inicio_str, hora_final_str = hora.split(' - ')
            hora_inicio = datetime.strptime(hora_inicio_str.strip(), '%I:%M %p').time()
            hora_final = datetime.strptime(hora_final_str.strip(), '%I:%M %p').time()

            HoraAgendada.objects.create(
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_final=hora_final,
                razon="Consulta general"
            )

            return redirect('confirmacion')

        except Exception as e:
            messages.error(request, f"Ocurrió un error: {e}")

    context = {
        'lunes_a_jueves': lunes_a_jueves,
        'viernes': viernes,
    }

    return render(request, 'Appclaudio/agendarHora.html', context)


@login_required
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
