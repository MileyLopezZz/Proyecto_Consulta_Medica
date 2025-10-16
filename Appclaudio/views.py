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

