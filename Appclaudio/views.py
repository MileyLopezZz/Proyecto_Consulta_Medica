from django.shortcuts import render
from .models import HoraAgendada

# Vista para mostrar la página de agendar cita
def agendar_hora(request):
    horarios_disponibles = {
        'Lunes a Jueves': [('10:30 AM', '01:00 PM'), ('03:00 PM', '07:00 PM')],
        'Viernes': [('10:30 AM', '01:00 PM')]
    }
    
    # Aquí puedes agregar la lógica para guardar la cita
    if request.method == 'POST':
        # Procesa los datos del formulario
        # Aquí puedes obtener los valores seleccionados y almacenarlos
        pass

    return render(request, 'Appclaudio/agendarHora.html', {'horarios_disponibles': horarios_disponibles})
# def agendar_hora_ok(request):
#     return render(request, 'Appclaudio/agendarHoraOk.html')