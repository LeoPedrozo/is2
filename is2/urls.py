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
from is2.views import inicio, saludo, documentaciones, step1_CrearRol, step2_CrearRol, crearSprint, step1_asignarRol, \
    step2_asignarRol, crearProyecto, \
    registrarUsuario, \
    modificarProyecto, verMiembros, eliminarRol, step1_modificarRol, step2_modificarRol, step3_modificarRol, \
    crearHistoria, verHistorias, \
    seleccionarHistoria, modificarHistoria, eliminarProyecto, eliminarHistoria, modificarSprint, visualizarSprint, \
    tableroKanban, moverHistoria, visualizarSprint2, lineChart, asignarHistoriaEncargado, asignarSprint, productBacklog, \
    swichProyecto, importarRol

#Librerias importadas del autenticador
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.urls import include, re_path


urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('bienvenida/',saludo), # hola mundo para probar si funciona el sistema
    path('documentacion/',documentaciones), #Todavia no implementado, para mostrar las documentaciones en la pagina

    path('crearRol/1/',step1_CrearRol),
    path('crearRol/2/',step2_CrearRol),

    path('asignarRol/1/', step1_asignarRol),
    path('asignarRol/2/', step2_asignarRol),


    path('eliminarRol/',eliminarRol),
    path('registrarUsuario/',registrarUsuario),

    path('crearProyecto/',crearProyecto),
    path('modificarProyecto/',modificarProyecto),
    path('eliminarProyecto/',eliminarProyecto),
    path('inicio/<int:id>/',swichProyecto),
    path('importarRoles/',importarRol),

    path('crearSprint/',crearSprint),
    path('modificarSprint/',modificarSprint),
    path('visualizarSprint/',visualizarSprint),

    path('visualizarSprint/<int:id>/',visualizarSprint2),

    path('crearHistoria/',crearHistoria),
    path('verHistorias/',productBacklog),
    path('verHistorias/<int:id>/',asignarSprint),

    path('modificarRol/1/',step1_modificarRol),
    path('modificarRol/2/',step2_modificarRol),
    path('modificarRol/3/',step3_modificarRol),

    path('modificarHistoria/1/',seleccionarHistoria),
    path('modificarHistoria/2/',modificarHistoria),
    path('eliminarHistoria/',eliminarHistoria),
    path('asignarEncargado/',asignarHistoriaEncargado),

    path('tableroKanban/',tableroKanban),

    path('tableroKanban/<int:id>/<int:opcion>/',moverHistoria),

    path('listarMiembros/',verMiembros),

    path('burndownChart/',lineChart),

    re_path(r'^docs/', include('docs.urls')),
    path('inicio/',inicio), #Pagina de inicio del sistema (Una vez loggeado)
    #Autenticador de google
    path('', TemplateView.as_view(template_name="index.html")), #Pagina de logeo (Boton iniciar sesion)
    path('accounts/', include('allauth.urls')), #Pagina SSO de Google mediante OAuth2
    #path('logout/', LogoutView.as_view(
    #next_page=reverse_lazy('Userauth:login') # you can use your named URL here just like you use the **url** tag in your django template
    #), name='logout'),

    path('inicio/logout', LogoutView.as_view()), #Funcion para deslogear del sistema
    path('logout/', LogoutView.as_view()),  # Funcion para deslogear del sistema
    path('accounts/google/login/callback/logout',LogoutView.as_view()) #Funcion para deslogear del sistema luego de autenticar

]