from django.urls import path
from . import views

urlpatterns = [
    path('ficha/', views.ficha_medica_view, name='ficha_medica'),
    path('buscar_paciente/', views.buscar_paciente, name='buscar_paciente'),
    path('pacientes/', views.paciente_view, name='paciente'),
    path('menuDoctor/', views.menu_doctor, name='menu_doctor'),
    path('loginDoctor/', views.login_doctor, name='login_doctor'),
    path('ficha/<int:id>/', views.ver_ficha, name='ver_ficha'),
    path('ficha/editar/<int:id>/', views.editar_ficha, name='editar_ficha'),
    path('ficha/eliminar/<int:id>/', views.eliminar_ficha, name='eliminar_ficha'),
    path('paciente/<int:id>/', views.detalle_paciente, name='detalle_paciente'),

]









