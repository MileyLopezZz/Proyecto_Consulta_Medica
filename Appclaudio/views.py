from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages

def agendar_hora_view(request):
    # Validar sesión 
    if not request.session.get('usuario_id'):
        messages.error(request, "Debes iniciar sesión para agendar una hora.")
        return redirect('login')

    horarios_disponibles = {}
    fecha_seleccionada = None
    horarios_dia = []

    # Si se envía una fecha, calculamos los horarios disponibles
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        motivo = request.POST.get('motivo')

        if fecha:
            fecha_seleccionada = datetime.strptime(fecha, "%Y-%m-%d")
            dia_semana = fecha_seleccionada.strftime('%A')  # Monday, Tuesday...

            if dia_semana in ['Monday', 'Tuesday', 'Wednesday', 'Thursday']:
                horarios_dia = ['10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM',
                                '3:00 PM', '3:30 PM', '4:00 PM', '5:00 PM', '6:00 PM']
            elif dia_semana == 'Friday':
                horarios_dia = ['10:30 AM', '11:00 AM', '12:00 PM']
            else:
                horarios_dia = []  # Sábado o domingo → sin atención

        # Confirmación de cita
        if motivo and fecha:
            messages.success(request, f"Tu cita fue agendada para {fecha} ({motivo}) ✅")
            return redirect('confirmacion')

    return render(request, 'Appclaudio/agendarHora.html', {
        'fecha_seleccionada': fecha_seleccionada,
        'horarios_dia': horarios_dia
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
