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

            # Ya NO se busca por RUT. Solo se guardan los datos ingresados manualmente
            ficha.nombre_paciente = form.cleaned_data.get('nombre_paciente')
            ficha.apellido_paciente = form.cleaned_data.get('apellido_paciente')
            ficha.telefono_paciente = form.cleaned_data.get('telefono_paciente')
            ficha.direccion_paciente = form.cleaned_data.get('direccion_paciente')
            ficha.prevision_paciente = form.cleaned_data.get('prevision_paciente')
            ficha.rut_paciente = rut

            ficha.save()
            return redirect('ficha_medica')

    else:
        form = FichaMedicaForm()

    return render(request, 'fichaMedica.html', {'form': form})


# 🔴 Se elimina completamente la función de búsqueda por RUT
# def buscar_paciente(request):
#     pass


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
                    paciente_existente.usuarios_id_usuario = request.user.id
                paciente_existente.save()
            else:
                paciente_nuevo = form.save(commit=False)
                if request.user.is_authenticated:
                    paciente_nuevo.usuarios_id_usuario = request.user.id
                paciente_nuevo.save()

            return redirect('paciente')
    else:
        form = PacienteForm()

    return render(request, 'pacientes.html', {'form': form})


def is_doctor_check(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name='Doctor').exists())


def menu_doctor(request):
    """
    Vista principal del dashboard del doctor, accesible directamente (sin credenciales).
    Carga datos simulados para el Dr. Constanzo.
    """
    
    # Datos simulados del Doctor
    doctor_data = {
        'full_name': 'Dr. Claudio Constanzo',
        'experience': '9 años de experiencia',
        'email': 'claudio.constanzo@clinica.cl',
        'phone': '+56 9 12345678',
        'license': 'Lic. CC-12345',
        'greeting': 'Dr. Constanzo',
    }

    # Lógica para obtener las 4 citas de hoy
    citas_hoy = [
        {'nombre': 'María González', 'hora': '10:00 AM', 'razon': 'Control de presión arterial', 'estado': 'Confirmado'},
        {'nombre': 'Carlos Rodríguez', 'hora': '10:30 AM', 'razon': 'Dolor de articulación', 'estado': 'Reprogramar'},
        {'nombre': 'Laura Sánchez', 'hora': '02:00 PM', 'razon': 'Evaluación anual', 'estado': 'Pendiente'},
        {'nombre': 'Roberta Díaz', 'hora': '03:00 PM', 'razon': 'Resultados de electrocardiograma', 'estado': 'Confirmado'},
    ]

    fichas_medicas = [
        {
            'id': '001A', 
            'paciente': 'Martina Flores C.', 
            'fecha': '20/09/2024', 
            'diagnostico': 'Control anual. Colesterol levemente elevado. Dieta recomendada.'
        },
        {
            'id': '002B', 
            'paciente': 'Sebastián Vidal P.', 
            'fecha': '05/10/2024', 
            'diagnostico': 'Consulta por resfriado común persistente. Reposo y paracetamol.'
        },
        {
            'id': '003C', 
            'paciente': 'Claudia Herrera R.', 
            'fecha': '15/08/2024', 
            'diagnostico': 'Revisión post-operatoria de apendicitis. Cicatrización normal. Retiro de puntos y alta médica.'
        },
        {
            'id': '004D', 
            'paciente': 'Javier Pérez L.', 
            'fecha': '10/07/2024', 
            'diagnostico': 'Migrañas crónicas. Ajuste de medicación preventiva. Se programa seguimiento en 30 días.'
        }
    ]
    
    # Lógica para obtener la lista de pacientes (para el select de Recetas)
    pacientes_list = [
        {'id': 1, 'nombre_completo': 'María González'},
        {'id': 2, 'nombre_completo': 'Carlos Rodríguez'},
        {'id': 3, 'nombre_completo': 'Laura Sánchez'},
        {'id': 4, 'nombre_completo': 'Roberta Díaz'},
        {'id': 5, 'nombre_completo': 'Felipe Torres'},
    ]
    
    context = {
        'citas_hoy': citas_hoy,
        'object_list': pacientes_list,
        'num_citas': len(citas_hoy),
        'doctor': doctor_data, # Pasamos el diccionario del doctor
        'fichas_medicas': fichas_medicas, # <-- NUEVO
    }
    
    return render(request, 'menuDoctor.html', context)
