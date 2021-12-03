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
from is2.views import inicio, saludo, documentaciones, step1_CrearRol, step2_CrearRol, step1_SprintPlanning, \
    step1_asignarRol, \
    step2_asignarRol, crearProyecto, \
    registrarUsuario, \
    modificarProyecto, verMiembros, step1_modificarRol, step2_modificarRol, step3_modificarRol, \
    crearHistoria, sprintBacklog, \
    seleccionarHistoria, modificarHistoria, eliminarProyecto, eliminarHistoria, modificarSprint, visualizarSprint, \
    tableroKanban, moverHistoria, visualizarSprint2, lineChart, asignarHistoriaEncargado, asignarSprint, productBacklog, \
    swichProyecto, importarRol, step1_eliminarRol, step2_eliminarRol, \
    search, swichProyecto, importarRol, step1_eliminarRol, step2_eliminarRol, step2_SprintPlanning, \
    asignarCapacidad, step3_SprintPlanning, step3_asignarEncargado, tableroQA_Release, eliminarSprint, moverHistoriaQA, \
    visualizarSprintFilter, historicoSprint, HistorialProyectoFilter, HistorialSprintFilter, \
    HistorialProductBacklog, BurndownChart, finalizarProyecto, iniciarProyecto, finalizarOexpandirSprint, infoProyecto, \
    infoUsuario, modificarProyecto2, tableroQA_Release2, modificarHistoria2, eliminarHistoria2, step1_SprintPlanning2, \
    step2_SprintPlanning2, asignarCapacidad2, step3_SprintPlanning2, step3_Funcionalidades, modificarSprint2, \
    sprintBacklog2, tableroKanban2, moverHistoria2, funcionalidadesQA, KanbanHistorico, eliminarSprint2, homeProyecto, \
    eliminarProyecto2, intercambiarMiembro, accesoDenegado, infoSprint, informe_US_ProductBacklog, informe_Sprint
from django.conf.urls import url


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
    path('AccesoDenegado/',accesoDenegado),

    #URL relacionados a roles y usuario
    path('crearRol/1/',step1_CrearRol), #ok
    path('crearRol/2/',step2_CrearRol), #ok
    path('modificarRol/1/', step1_modificarRol), #ok
    path('modificarRol/2/', step2_modificarRol), #ok
    path('modificarRol/3/', step3_modificarRol), #ok
    path('asignarRol/1/', step1_asignarRol), #ok
    path('asignarRol/2/', step2_asignarRol), #ok
    path('eliminarRol/1/',step1_eliminarRol), #ok
    path('eliminarRol/2/',step2_eliminarRol), #ok
    path('registrarUsuario/',registrarUsuario), #ok
    path('Usuario/<int:id_usuario>/info/',infoUsuario),

    #URL relacionado a proyecto
    path('proyecto/nuevo/',crearProyecto), #ok only superuser
    #path('proyecto/',HistorialProyectoFilter),
    path('proyecto/<int:id_proyecto>/',homeProyecto),#
    path('proyecto/<int:id_proyecto>/Sprints/', HistorialSprintFilter),
    path('proyecto/<int:id_proyecto>/ProductBacklog/', HistorialProductBacklog),
    path('proyecto/<int:id_proyecto>/Finalizar/', finalizarProyecto), #ok
    path('proyecto/<int:id_proyecto>/iniciar/', iniciarProyecto), #ok
    path('proyecto/<int:id_proyecto>/modificar/', modificarProyecto2),
    path('proyecto/<int:id_proyecto>/Resumen/',infoProyecto),
    path('proyecto/<int:id_proyecto>/eliminar/',eliminarProyecto2), #ok
    path('importarRoles/',importarRol),
    path('inicio/<int:id>/',swichProyecto),


    #NUEVOS URLS relacionados a Historia

    path('proyecto/<int:id_proyecto>/ProductBacklog/nuevo/', crearHistoria),
    path('proyecto/<int:id_proyecto>/ProductBacklog/modificar/Historia<int:id_historia>/', modificarHistoria2),
    path('proyecto/<int:id_proyecto>/ProductBacklog/Eliminar/Historia<int:id_historia>/', eliminarHistoria2),


    #NUEVOS URLS  relacionados al Manejo de Sprint.
         #estos paths son de crear nuevo sprint
    path('proyecto/<int:id_proyecto>/Sprints/nuevo/InformacionBasica/', step1_SprintPlanning2),
        #esto no se usa
    path('proyecto/<int:id_proyecto>/Sprints/nuevo/FormarEquipo/', step2_SprintPlanning),
    path('proyecto/<int:id_proyecto>/Sprints/nuevo/AsignarHistorias/', step3_SprintPlanning),
    path('proyecto/<int:id_proyecto>/Sprints/nuevo/FormarEquipo/<int:id_usuario>', asignarCapacidad),
    #ojo
    #path('proyecto/<int:id_proyecto>/Sprints/nuevo/AsignarEncargado/<int:id>/<int:opcion>/', step3_asignarEncargado),

        #estos paths son de modificar.
    path('proyecto/<int:id_proyecto>/Sprints/modificar/<int:id_sprint>/InformacionBasica/',modificarSprint2),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/FormarEquipo/', step2_SprintPlanning2),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/AsignarHistorias/', step3_SprintPlanning2),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/FormarEquipo/<int:id_usuario>/<str:opcion>', asignarCapacidad2),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/AsignarEncargado/Historia<int:id_historia>/Op<int:opcion>/', step3_Funcionalidades),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/Eliminar/', eliminarSprint2), #ok
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/info/', infoSprint), #ok


    #URL relacionados a los aspectos relacionados al sprint
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/SprintBacklog/',sprintBacklog2),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/KanbanActivo/',tableroKanban2), # FalTa
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/KanbanActivo/Historia<int:id_historia>/Op<int:opcion>', moverHistoria2), #Falta
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/BurndownChart/',BurndownChart),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/KanbanActivo/accion+<str:opcion>/',finalizarOexpandirSprint),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/intercambiar/',intercambiarMiembro),


    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/QualityAssurance/',tableroQA_Release2),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/QualityAssurance/<int:id_historia>/<int:opcion>/', funcionalidadesQA),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/kanbanHistorico/',KanbanHistorico),
    path('proyecto/<int:id_proyecto>/exportUS/', informe_US_ProductBacklog),
    path('proyecto/<int:id_proyecto>/Sprints/<int:id_sprint>/exportUS/', informe_Sprint),

    #----------------------------------OLD URLS------------------------------------------


    #Url ya desactualizado
    path('tableroKanban/<int:id_sprint>/<str:opcion>/', finalizarOexpandirSprint),
    path('tableroKanban/', tableroKanban),
    path('tableroKanban/<int:id>/<int:opcion>/', moverHistoria),
    #URL RELACIONADAS A SPRINT
    path('SprintPlanning/1/', step1_SprintPlanning),
    #path('proyecto/<int:id_proyecto>/Sprints/nuevo/InformacionBasica/', step1_SprintPlanning),

    path('SprintPlanning/2/', step2_SprintPlanning),
    #path('proyecto/<int:id_proyecto>/Sprints/nuevo/FormarEquipo/', step2_SprintPlanning),
    path('SprintPlanning/2/<int:id>/', asignarCapacidad),
    #path('proyecto/<int:id_proyecto>/Sprints/nuevo/FormarEquipo/<int:id_usuario>', asignarCapacidad),

    path('SprintPlanning/3/', step3_SprintPlanning),
    #path('proyecto/<int:id_proyecto>/Sprints/nuevo/AsignarHistoria/', step3_SprintPlanning),

    path('SprintPlanning/3/<int:id>/<int:opcion>/', step3_asignarEncargado),
    #path('proyecto/<int:id_proyecto>/Sprints/nuevo/AsignarHistoria/<int:id_historia>/<int:opcion>/', step3_asignarEncargado),

    path('sprintBacklog/<int:id_sprint>/',sprintBacklog),
    #path('sprint/<int:id_sprint>/BackLog/',sprintBacklog),

    path('modificarSprint/<int:id_sprint>/',modificarSprint),
    #path('sprint/<int:id_sprint>/modificar/',modificarSprint),
    path('eliminarSprint/<int:id_sprint>/',eliminarSprint),

    #ya no se usa
    path('visualizarSprint/',visualizarSprint),
    #ya no se usa
    path('visualizarSprint/<int:id>/',visualizarSprint2),
    #path('KanBan/Historico/<int:id>/',visualizarSprint2),

    #URL relacionada a historias
    path('modificarHistoria/1/', seleccionarHistoria),
    path('modificarHistoria/2/', modificarHistoria),
    path('eliminarHistoria/', eliminarHistoria),


    # no se usa mas
    path('modificarProyecto/', modificarProyecto),
    path('eliminarProyecto/', eliminarProyecto),

    path('verHistorias/',productBacklog),
    path('verHistorias/<int:id>/',asignarSprint),
    path('asignarEncargado/',asignarHistoriaEncargado),
    #path('tableroKanban/<str:opcion>/',tableroKanban),



    path('listarMiembros/',verMiembros),
    #path('burndownChart/',lineChart),

    path('burndownChart/<int:id_sprint>/',BurndownChart),
    #path('sprint/<int:id_sprint>/BurndownChart/',BurndownChart),

    #path('historicooSprint/<int:id_sprint>/',historicoSprint2),
    #path('sprint/<int:id>/KanBan/Historico/',historicoSprint2),

    #URL relacionado a la tablero QA
    path('qualityassurance/<int:id_sprint>/',tableroQA_Release2),
    #path('sprint/<int:id_sprint>/QualityAssurance/',tableroQA_Release2),
    path('qaRelease/<int:id>/<int:id_sprint>/<int:opcion>/', moverHistoriaQA),
    #path('sprint/<int:id_sprint>/QuealityAssurance/<int:opcion>/<int:id>/', moverHistoriaQA),

    #viejo ya no se usan
    path('qaRelease/<int:id>/', tableroQA_Release),
    path('qaRelease/', tableroQA_Release),


    url(r'^productBacklog/$', search, name='search'),


    path('productBacklog/<int:id>/', asignarSprint),

    path('historicoSprint/<int:id>/', historicoSprint, name='historicoSprint'),
    path('historicoSprint/', historicoSprint, name='historicoSprint'),
    url(r'^historialSprint/$', visualizarSprintFilter, name='visualizarSprintFilter'),





    re_path(r'^docs/', include('docs.urls')),
    #path('inicio/',inicio), #Pagina de inicio del sistema (Una vez loggeado)

    path('inicio/',inicio),


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