"""is2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/

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

from django.contrib import admin
from django.urls import path
from is2.views import inicio, saludo, documentaciones, crearRol, crearSprint, asignarRol, crearProyecto, \
    registrarUsuario, \
    modificarProyecto, verMiembros, eliminarRol, seleccionarRol, modificarRol

#Librerias importadas del autenticador
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('bienvenida/',saludo), # hola mundo para probar si funciona el sistema
    path('documentacion/',documentaciones), #Todavia no implementado, para mostrar las documentaciones en la pagina

    path('crearRol/',crearRol),
    path('asignarRol/',asignarRol),
    path('eliminarRol/',eliminarRol),
    path('registrarUsuario/',registrarUsuario),
    path('crearProyecto/',crearProyecto),
    path('modificarProyecto/',modificarProyecto),
    path('crearSprint/',crearSprint),

    path('modificarRol/1/',seleccionarRol),
    path('modificarRol/2/',modificarRol),

    path('listarMiembros/',verMiembros),

    path('accounts/google/login/callback/inicio/',inicio), #Pagina de inicio del sistema (Una vez loggeado)
    #Autenticador de google
    path('', TemplateView.as_view(template_name="index.html")), #Pagina de logeo (Boton iniciar sesion)
    path('accounts/', include('allauth.urls')), #Pagina SSO de Google mediante OAuth2
    path('logout', LogoutView.as_view()), #Funcion para deslogear del sistema
    path('accounts/google/login/callback/inicio/logout',LogoutView.as_view()) #Funcion para deslogear del sistema luego de autenticar

]