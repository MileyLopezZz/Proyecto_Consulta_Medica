from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import FichaMedicaForm, PacienteForm
from .models import Paciente, FichaMedica
from django.contrib.auth.models import AnonymousUser


# --------------------- FICHA MÉDICA ---------------------
def ficha_medica_view(request):
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data.get('rut_paciente')
            ficha = form.save(commit=False)

            try:
                paciente = Paciente.objects.get(rut=rut)
                # Rellena automáticamente los datos del paciente si existe
                ficha.nombre_paciente = paciente.nombre
                ficha.apellido_paciente = paciente.apellido
                ficha.telefono_paciente = paciente.telefono
                ficha.direccion_paciente = paciente.direccion
                ficha.prevision_paciente = paciente.prevision
            except Paciente.DoesNotExist:
                # Si no existe, usa los datos ingresados manualmente
                ficha.nombre_paciente = form.cleaned_data.get('nombre_paciente')
                ficha.apellido_paciente = form.cleaned_data.get('apellido_paciente')
                ficha.telefono_paciente = form.cleaned_data.get('telefono_paciente')
                ficha.direccion_paciente = form.cleaned_data.get('direccion_paciente')
                ficha.prevision_paciente = form.cleaned_data.get('prevision_paciente')

            ficha.save()
            return redirect('ficha_medica')

    else:
        form = FichaMedicaForm()

    return render(request, 'fichaMedica.html', {'form': form})


def buscar_paciente(request):
    """Busca un paciente por RUT (usado por AJAX en ficha médica)."""
    rut = request.GET.get('rut', '').strip()
    if rut:
        try:
            paciente = Paciente.objects.get(rut=rut)
            data = {
                'nombre': paciente.nombre,
                'apellido': paciente.apellido,
                'telefono': paciente.telefono,
                'direccion': paciente.direccion,
                'prevision': paciente.prevision,
                'rut': paciente.rut,
            }
            return JsonResponse(data)
        except Paciente.DoesNotExist:
            return JsonResponse({'error': 'Paciente no encontrado'})
    return JsonResponse({'error': 'No se proporcionó RUT'})


# --------------------- PACIENTES ---------------------
def paciente_view(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data.get('rut')
            paciente_existente = Paciente.objects.filter(rut=rut).first()

            if paciente_existente:
                for campo, valor in form.cleaned_data.items():
                    setattr(paciente_existente, campo, valor)
                # Asigna usuario solo si hay sesión activa
                if request.user.is_authenticated:
                    paciente_existente.usuarios_id_usuario = request.user
                paciente_existente.save()
            else:
                paciente_nuevo = form.save(commit=False)
                if request.user.is_authenticated:
                    paciente_nuevo.usuarios_id_usuario = request.user
                paciente_nuevo.save()

            return redirect('paciente')
    else:
        form = PacienteForm()

    return render(request, 'pacientes.html', {'form': form})




