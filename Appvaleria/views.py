from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from .forms import FichaMedicaForm, PacienteForm
from .models import Paciente, FichaMedica, CitaMedica
from datetime import date
from django.db import connection


# --------------------- CRUD FICHA MÉDICA ---------------------
def ficha_medica_view(request):
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.save()
            messages.success(request, "Ficha médica creada correctamente.")
            return redirect('menu_doctor')
    else:
        form = FichaMedicaForm()
    return render(request, 'fichaMedica.html', {'form': form})


def editar_ficha(request, id):
    ficha = get_object_or_404(FichaMedica, id_ficha=id)
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST, instance=ficha)
        if form.is_valid():
            form.save()
            messages.success(request, "Ficha médica actualizada correctamente.")
            return redirect('menu_doctor')
    else:
        form = FichaMedicaForm(instance=ficha)
    return render(request, 'fichaMedica.html', {'form': form, 'editar': True})


def eliminar_ficha(request, id):
    ficha = get_object_or_404(FichaMedica, id_ficha=id)
    ficha.delete()
    messages.warning(request, "Ficha médica eliminada correctamente.")
    return redirect('menu_doctor')


def ver_ficha(request, id):
    ficha = get_object_or_404(FichaMedica, id_ficha=id)
    return render(request, 'detalleFicha.html', {'ficha': ficha})


# --------------------- BÚSQUEDA DE PACIENTES ---------------------
def buscar_paciente(request):
    rut = request.GET.get('rut')
    try:
        paciente = Paciente.objects.get(rut=rut)
        data = {
            'nombre': paciente.nombre,
            'apellido': paciente.apellido,
            'telefono': paciente.telefono,
            'direccion': paciente.direccion,
        }
        return JsonResponse(data)
    except Paciente.DoesNotExist:
        return JsonResponse({'error': 'Paciente no encontrado'}, status=404)


# --------------------- CRUD PACIENTES ---------------------
def paciente_view(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data.get('rut')
            paciente_existente = Paciente.objects.filter(rut=rut).first()

            if paciente_existente:
                for campo, valor in form.cleaned_data.items():
                    setattr(paciente_existente, campo, valor)
                paciente_existente.save()
            else:
                form.save()

            messages.success(request, "Paciente guardado correctamente.")
            return redirect('paciente')
    else:
        form = PacienteForm()

    return render(request, 'pacientes.html', {'form': form})


# --------------------- MENÚ DOCTOR ---------------------
from django.db.models import Q
from django.db import connection
from .models import Paciente, FichaMedica

def menu_doctor(request):
    from datetime import date
    hoy = date.today()

    doctor_data = {
        'full_name': 'Dr. Claudio Constanzo',
        'experience': '9 años de experiencia',
        'email': 'claudio.constanzo@clinica.cl',
        'phone': '+56 9 12345678',
        'license': 'Lic. CC-12345',
        'greeting': 'Dr. Constanzo',
    }

    # --- Citas del día ---
    from .models import FichaMedica
    citas_hoy = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT h.id_hora, p.nombre, p.apellido, h.hora_inicio, h.hora_final, h.razon, h.estado
                FROM hora_agendada h
                JOIN paciente p ON p.id_paciente = h.paciente_id
                WHERE DATE(h.hora_inicio) = CURDATE()
                ORDER BY h.hora_inicio ASC;
            """)
            citas_hoy = cursor.fetchall()
    except Exception:
        citas_hoy = []

    # --- Fichas médicas recientes ---
    fichas_medicas = FichaMedica.objects.all().order_by('-hora_ficha')[:5]

    # --- Búsqueda de pacientes ---
    query = request.GET.get('buscar', '').strip()
    pacientes = []
    if query:
        pacientes = Paciente.objects.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=query) | Q(rut__icontains=query)
        )

    context = {
        'doctor': doctor_data,
        'fichas_medicas': fichas_medicas,
        'citas_hoy': citas_hoy,
        'num_citas': len(citas_hoy),
        'buscar': query,
        'pacientes': pacientes,
    }
    return render(request, 'menuDoctor.html', context)



# --------------------- LOGIN ---------------------
def login_doctor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        correo_doctor = "doctor@gmail.com"
        clave_doctor = "doctor1234"

        if email == correo_doctor and password == clave_doctor:
            messages.success(request, "Bienvenido doctor.")
            return redirect('menu_doctor')
        else:
            messages.error(request, "Correo o contraseña incorrectos.")

    return render(request, 'loginDoctor.html')



def buscar_paciente_doctor(request):
    query = request.GET.get('buscar', '').strip()
    paciente = None
    fichas = []
    citas = []

    if query:
        # Buscar paciente por nombre, apellido o rut
        paciente = Paciente.objects.filter(
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) | 
            Q(rut__icontains=query)
        ).first()

        if paciente:
            # Fichas médicas asociadas
            fichas = FichaMedica.objects.filter(rut_paciente=paciente.rut).order_by('-hora_ficha')

            # Horas agendadas del paciente (desde tabla hora_agendada)
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT hora_inicio, hora_final, razon, estado 
                    FROM hora_agendada 
                    WHERE paciente_id = %s 
                    ORDER BY hora_inicio DESC
                """, [paciente.id_paciente])
                citas = cursor.fetchall()

    context = {
        'paciente': paciente,
        'fichas': fichas,
        'citas': citas,
        'buscar': query,
    }

    return render(request, 'buscarPaciente.html', context)


def detalle_paciente(request, id):
    # Buscar el paciente por su ID
    paciente = get_object_or_404(Paciente, id_paciente=id)

    # Fichas médicas asociadas
    fichas = FichaMedica.objects.filter(rut_paciente=paciente.rut).order_by('-hora_ficha')

    # Citas agendadas (tabla hora_agendada)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT hora_inicio, hora_final, razon, estado
            FROM hora_agendada
            WHERE paciente_id = %s
            ORDER BY hora_inicio DESC
        """, [paciente.id_paciente])
        citas = cursor.fetchall()

    context = {
        'paciente': paciente,
        'fichas': fichas,
        'citas': citas,
    }
    return render(request, 'detallePaciente.html', context)


