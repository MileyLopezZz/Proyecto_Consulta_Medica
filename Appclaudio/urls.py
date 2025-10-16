from django.urls import path
from . import views

urlpatterns = [
    path('agendarHora/', views.agendar_hora_view, name='agendarhora'),
    path('confirmacion/', views.confirmacion_view, name='confirmacion'),
]
