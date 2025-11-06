from django.urls import path
from . import views

urlpatterns = [
    path('ficha/', views.ficha_medica_view, name='ficha_medica'),
    path('buscar_paciente/', views.buscar_paciente, name='buscar_paciente'),
    path('pacientes/', views.paciente_view, name='paciente'),
    path('menuDoctor/', views.menu_doctor, name='menu_doctor'),
    path('loginDoctor/', views.login_doctor, name='login_doctor'),
]
