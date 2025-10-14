from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.RegisterUser, name='registro'),
    path('login/', views.loginUser, name= 'login'),
    path('vistaUsuario/', views.UserView, name= 'UsuarioView')
]
