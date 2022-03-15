"""controle_beneficios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from registros.views import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

usuarios_urls = [
    path('usuario/cadastro/', CriarUsusarioView.as_view(),name="cadastro_usuario"),
    path('usuario/login/', LoginView.as_view(),name="logar"),
    path('usuario/logout/', LogoutView.as_view(),name="deslogar"),
]

urlpatterns = [
    path('', HomeView.as_view(),name="home"),
    path('registros/filtro/', login_required(RegistrosFiltroView.as_view()),name="registros_filtro"),
    path('registros/filtro/<int:pk>/', login_required(RegistrosFiltroView.as_view()),name="registros_filtro"),
    path('registros/novo/', login_required(RegistrarView.as_view()),name="registrar"),
    path('registros/adicionar/<int:pk>/', login_required(AdicionarRegistroView.as_view()),name="adicionar_registro"),
    path('registros/todos/', login_required(TodosRegistrosView.as_view()),name="todos_registros"),
    path('registros/beneficiado/<int:pk>/', login_required(BeneficiadoDadoslView.as_view()),name="beneficiado"),
    path('registros/beneficiado/editar/<int:pk>/', login_required(BeneficiadoEditView.as_view()),name="editar_beneficiado"),
]+usuarios_urls