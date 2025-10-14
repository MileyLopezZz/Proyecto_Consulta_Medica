from django.urls import path
from . import views

urlpatterns = [
    path('agendarHora/', views.agendar_hora, name='agendarhora'),
    # path("ok/", views.agendar_hora_ok, name="agendar_hora_ok"),
]
