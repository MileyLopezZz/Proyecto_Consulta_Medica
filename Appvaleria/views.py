from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import FichaMedicaForm
from .models import Paciente, FichaMedica

def ficha_medica_view(request):
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data.get('rut_paciente')
            ficha = form.save(commit=False)
            try:
                paciente = Paciente.objects.get(rut=rut)
                ficha.paciente = paciente
                ficha.nombre_paciente = paciente.nombre
                ficha.apellido_paciente = paciente.apellido
                ficha.telefono_paciente = paciente.telefono
                ficha.direccion_paciente = paciente.direccion
                ficha.rut_paciente = paciente.rut
                ficha.prevision_paciente = paciente.prevision
            except Paciente.DoesNotExist:
                ficha.nombre_paciente = form.cleaned_data.get('nombre_paciente')
                ficha.apellido_paciente = form.cleaned_data.get('apellido_paciente')
                ficha.telefono_paciente = form.cleaned_data.get('telefono_paciente')
                ficha.direccion_paciente = form.cleaned_data.get('direccion_paciente')
                ficha.rut_paciente = rut
                ficha.prevision_paciente = form.cleaned_data.get('prevision_paciente')
            ficha.save()
            return redirect('ficha_medica')
    else:
        form = FichaMedicaForm()
    return render(request, 'fichaMedica.html', {'form': form})





def buscar_paciente(request):
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
                'rut': paciente.rut
            }
            return JsonResponse(data)
        except Paciente.DoesNotExist:
            return JsonResponse({'error': 'Paciente no encontrado'})
    return JsonResponse({'error': 'No se proporcionó RUT'})

