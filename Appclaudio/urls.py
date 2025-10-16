from django.urls import path
from . import views
from .views import listar_secretarias, crear_secretaria, editar_secretaria, eliminar_secretaria


urlpatterns = [
    path('agendarHora/', views.agendar_hora_view, name='agendarhora'),
    path('confirmacion/', views.confirmacion_view, name='confirmacion'), 
    path('secretarias/', listar_secretarias, name='listar_secretarias'),
    path('secretarias/crear/', crear_secretaria, name='crear_secretaria'),
    path('secretarias/editar/<int:pk>/', editar_secretaria, name='editar_secretaria'),
    path('secretarias/eliminar/<int:pk>/', eliminar_secretaria, name='eliminar_secretaria'),

]
