import requests
from django.forms import model_to_dict
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import date, datetime, timedelta
from workalendar.america import Paraguay

from django.http import HttpResponse
from django.db import models

from django.template import Template, Context
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from GestionPermisos.forms import crearRolForm, asignarRolForm, registroDeUsuariosForm, seleccionarRolForm, \
    modificarRolForm
from GestionPermisos.views import fabricarRol, enlazar_Usuario_con_Rol, registrar_usuario, removerRol
from Sprints.views import nuevoSprint,updateSprint,sprintActivoen,guardarCamposdeSprint,getSprint
from gestionUsuario.models import User
from gestionUsuario.views import asociarProyectoaUsuario, desasociarUsuariodeProyecto
from proyectos.views import nuevoProyecto, getProyecto, updateProyecto,guardarCamposdeProyecto
from proyectos.forms import crearproyectoForm, modificarproyectoForm, eliminarProyectoForm
from proyectos.models import Proyecto
from proyectos.forms import crearproyectoForm, modificarproyectoForm,eliminarProyectoForm
from django.contrib.auth.decorators import user_passes_test
from Sprints.forms import crearSprintForm, modificarSprintForm, visualizarSprintForm
from userStory.forms import crearHistoriaForm, seleccionarHistoriaForm, modificarHistoriaForm, eliminarHistoriaForm, cargarHorasHistoriaForm
from userStory.models import Historia
from userStory.views import nuevaHistoria, updateHistoria


# Hola mundo para probar django
@login_required
def saludo(request):
    """
    Metodo que es ejecutado para mostrar un mensaje de saludo al usuario loggeado en el sistema

    :param request: consulta recibida
    :return: respuesta
    """
    return render(request, "rolCreado.html", {"nombre": "Jose"})


def inicio(request):
    """
    Metodo que es ejecutado para mostrar la pagina de inicio del sistema

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de INICIO
    """
    if request.user.groups.filter(name='registrado'):
        print("el usuario pertenece al grupo de registrados")
        if request.user.is_superuser:
            return render(request, "sidenav.html", {"avatar": None})
        else:
            fotodeususario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']
            return render(request, "sidenav.html", {"avatar": fotodeususario})
    else:
        return render(request, "registroRequerido.html", {"mail": request.user.email})


# Para acceder directamente a los archivos guardados en el directorio docs
# (Todavia no se ha implementado)
def documentaciones(request):
    """
    Metodo para acceder directamente a los archivos referentes a la documentacion del sistema

    :param request: consulta recibida
    :return: respuesta: de redireccionamiento
    """
    return render(request, "html/index.html", {})


##VISTAS RELACIONADAS AL MANEJO DE ROL
@login_required
@permission_required('auth.add_group', raise_exception=True)
def crearRol(request):
    """
    Metodo para la creacion de roles del sistema

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR ROL
    """
    if request.method == "POST":
        formulario = crearRolForm(request.POST)
        if (formulario.is_valid()):
            datosRol = formulario.cleaned_data

            print(formulario.cleaned_data)

            nombreRol = formulario.cleaned_data["RolName"]
            historia = formulario.cleaned_data["Historia"]
            proyecto = formulario.cleaned_data["Proyecto"]
            sprint = formulario.cleaned_data["Sprint"]

            # Acciones a realizar con el form
            fabricarRol(datosRol)
            # Retornar mensaje de exito
            return render(request, "rolCreado.html",
                          {"nombreRol": nombreRol, "historia": historia, "proyecto": proyecto, "sprint": sprint})
    else:
        formulario = crearRolForm()

    return render(request, "crearRol.html", {"form": formulario})

@login_required
@permission_required('auth.add_group', raise_exception=True)
def asignarRol(request):
    """
    Metodo para la asignacion de roles a los usuarios del sistema

    :param request: solicitud recibida
    :return: respuesta: a la solicitud de ASIGNAR ROL
    """
    if request.method == "POST":
        formulario = asignarRolForm(request.POST)
        if (formulario.is_valid()):
            datosRol = formulario.cleaned_data
            userdata = formulario.cleaned_data['Usuario']
            rol = formulario.cleaned_data['Roles']
            # Acciones a realizar con el form

            enlazar_Usuario_con_Rol(userdata, rol)

            # Retornar mensaje de exito
            return render(request, "outputAsignarRol.html", {"asignaciondeRol": datosRol})
    else:
        formulario = asignarRolForm()

    return render(request, "asignarRol.html", {"form": formulario})

@login_required
@permission_required('auth.delete_group', raise_exception=True)
def eliminarRol(request):
    """
        Metodo para la asignacion de roles a los usuarios del sistema

        :param request: solicitud recibida
        :return: respuesta: a la solicitud de ASIGNAR ROL
        """
    if request.method == "POST":
        formulario = seleccionarRolForm(request.POST)
        if (formulario.is_valid()):
            RolSeleccionado = formulario.cleaned_data['Rol']

            print(formulario.cleaned_data)

            # Acciones a realizar con el form
            removerRol(RolSeleccionado)
            # Retornar mensaje de exito
            return render(request, "outputEliminarRol.html", {"roleliminado": RolSeleccionado})
    else:
        formulario = seleccionarRolForm()

    return render(request, "eliminarRol.html", {"form": formulario})


# modificar Rol 1
@login_required
@permission_required('auth.add_group', raise_exception=True)
def seleccionarRol(request):
    """
        Metodo para la asignacion de roles a los usuarios del sistema

        :param request: solicitud recibida
        :return: respuesta: a la solicitud de ASIGNAR ROL
        """
    if request.method == "POST":
        formulario = seleccionarRolForm(request.POST)
        if (formulario.is_valid()):
            RolSeleccionado = formulario.cleaned_data['Rol']
            modeloRol = model_to_dict(RolSeleccionado)
            print("Modelo Rol: ")
            print(modeloRol)

            request.session['RolSeleccionado_id'] = modeloRol['id']
            request.session['nombreRol'] = modeloRol['name']

            getPermisos(request, modeloRol['permissions'])
            print("Permisos obtenidos")

            return redirect(modificarRol)
    else:
        formulario = seleccionarRolForm()

    return render(request, "seleccionarRol.html", {"form": formulario})


# modificar Rol 2
@login_required
@permission_required('auth.change_group', raise_exception=True)
def modificarRol(request):
    """
    Metodo para la modificacion de roles

    :param request: solicitud recibida
    :return: respuesta a la solicitud de MODIFICAR ROL
    """
    if request.method == "POST":

        formulario = modificarRolForm(request.POST, datosdelRol=request.session)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosNuevos = formulario.cleaned_data
            print("cleaned data de los datos de Rol cambiados ", datosNuevos)
            # Obtener los usuarios que pertenecen al viejo rol, buscando por la id del rol
            viejoRol_id = request.session['RolSeleccionado_id']
            # Se estira los usuarios que forman parte al viejo Rol
            usuarios = User.objects.filter(groups__id=viejoRol_id)

            # Se elimina el viejo Rol
            modeloViejoRol = Group.objects.filter(id=viejoRol_id)
            modeloViejoRol.delete()

            # Se crea el nuevo Rol con sus respectivos permisos
            nombreRol = datosNuevos['RolName']
            nuevoRol = fabricarRol(datosNuevos)

            # Se enlazan los usuarios del viejo Rol al nuevo Rol
            for usuario in usuarios:
                enlazar_Usuario_con_Rol(usuario, nuevoRol)

            # Retornar mensaje de exito
            return render(request, "outputmodificarRol.html", {"rolModificado": datosNuevos, "nombreRol": nombreRol})
    else:

        formulario = modificarRolForm(datosdelRol=request.session)

    return render(request, "modificarRol.html", {"form": formulario})

@login_required
@staff_member_required
def registrarUsuario(request):
    """
    Metodo para registrar usuarios al sistema

    :param request: solicitud recibida
    :return: respuesta: a la solicitud de REGISTRAR USUARIO
    """
    if request.method == "POST":
        formulario = registroDeUsuariosForm(request.POST)
        if (formulario.is_valid()):
            datos = formulario.cleaned_data
            userdata = formulario.cleaned_data['Usuario']
            estado = formulario.cleaned_data['Habilitado']
            # Acciones a realizar con el form
            registrar_usuario(userdata, estado)

            # Retornar mensaje de exito
            return render(request, "outputRegistrarUsuario.html", {"usuario": datos})
    else:
        formulario = registroDeUsuariosForm()

    return render(request, "RegistrarUsuario.html", {"form": formulario})


# VISTAS RELACIONADAS AL MANEJO DE PROYECTOS
@login_required
@permission_required('proyectos.add_proyecto', raise_exception=True)
def crearProyecto(request):
    """
    Metodo para la creacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR PROYECTO
    """
    if request.method == "POST":
        ##instance = User.objects.filter(user=request.user).first()

        formulario = crearproyectoForm(request.POST, request=request)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosProyecto = formulario.cleaned_data
            miembros = formulario.cleaned_data["miembros"]
            proyecto = nuevoProyecto(formulario.cleaned_data)
            # proyecto = getProyecto(formulario.cleaned_data['nombre'])
            asociarProyectoaUsuario(proyecto, miembros)
            # Retornar mensaje de exito
            return render(request, "outputcrearProyecto.html", {"proyectoCreado": datosProyecto})
    else:
        formulario = crearproyectoForm(request=request)

    return render(request, "crearProyecto.html", {"form": formulario})


@login_required
@permission_required('proyectos.change_proyecto', raise_exception=True)
def modificarProyecto(request):
    """
    Metodo para la modificacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR PROYECTO
    """
    print("request modificar proyecto")

    try:
        if request.method == "POST":
            formulario = modificarproyectoForm(request.POST, request=request.session)
            if (formulario.is_valid()):
                # Acciones a realizar con el form
                idproyecto = formulario.cleaned_data['id']
                datosProyecto = formulario.cleaned_data

                miembros = formulario.cleaned_data["miembros"]
                usuarios = formulario.cleaned_data["usuarios"]

                updateProyecto(formulario.cleaned_data)

                proyecto = getProyecto(idproyecto)

                # se agrega los usuarios nuevos
                asociarProyectoaUsuario(proyecto, usuarios)
                # se elimina los usuarios viejos
                desasociarUsuariodeProyecto(miembros)

                miembrosActuales = User.objects.all().filter(proyecto=idproyecto)
                # Retornar mensaje de exito
                return render(request, "outputmodificarProyecto.html", {"proyectoCreado": datosProyecto, "members":miembrosActuales})
        else:
            usuarioActual = User.objects.get(username=request.user.username)
            if (usuarioActual.proyecto == None):
                mensaje = "Usted no forma parte de ningun proyecto"
                return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
            else:
                guardarCamposdeProyecto(request, usuarioActual)
                formulario = modificarproyectoForm(request=request.session)
                return render(request, "modificarProyecto.html", {"form": formulario})
    except AttributeError:
        print("El usuario no posee ningun proyecto")
        messages.error(request,'El usuario no posee ningun proyecto')
        return redirect(inicio)

@login_required
@permission_required('proyectos.delete_proyecto', raise_exception=True)
def eliminarProyecto(request):
    """
        Metodo para la asignacion de roles a los usuarios del sistema

        :param request: solicitud recibida
        :return: respuesta: a la solicitud de ASIGNAR ROL
    """
    if request.method == "POST":
        formulario = eliminarProyectoForm(request.POST)
        if (formulario.is_valid()):
            ProyectoSeleccionado = formulario.cleaned_data['Proyecto']

            #eliminamos todas las historias asociadas a este proyecto
            id_proyecto=ProyectoSeleccionado.id
            Historia.objects.filter(proyecto=id_proyecto).delete()

            #eliminamos los sprints

            proyecto=model_to_dict(ProyectoSeleccionado)
            sprints = proyecto["id_sprints"]
            for s in sprints:
                s.delete()


            historias=Historia.objects.filter(proyecto=id_proyecto)
            for h in historias:
                h.delete()

            #desasociamos los ususarios del proyecto
            miembros=User.objects.filter(proyecto_id=id_proyecto).exclude(
            username='admin')

            #desasociamos proyecto con ususario
            desasociarUsuariodeProyecto(miembros)

            # Eliminamos proyecto
            ProyectoSeleccionado.delete()

            # Retornar mensaje de exito
            return render(request, "outputEliminarProyecto.html", {"Proyectoeliminado": ProyectoSeleccionado})
    else:
        formulario = eliminarProyectoForm()

    return render(request, "eliminarProyecto.html", {"form": formulario})


@login_required
def getPermisos(request, listaPermisos):
    """
    Metodo de gestion y asignacion de permisos para los usuarios del sistema

    :param request: solicitud recibida
    :param listaPermisos: lista de permisos a ser distribuidos
    :return: respuesta a la solicitud de ejecucion recibida para el metodo GETPERMISOS
    """
    listaProyecto = []
    listaHistoria = []
    listaSprint = []

    for objeto_permiso in listaPermisos:
        lista = (str(objeto_permiso)).split("|")

        categoria = lista[1]
        permiso = lista[2]

        if (permiso.find(' Can add Proyecto') >= 0):
            listaProyecto.append("add")
        if (permiso.find(' Can change Proyecto') >= 0):
            listaProyecto.append("change")
        if (permiso.find(' Can delete Proyecto') >= 0):
            listaProyecto.append("delete")
        if (permiso.find(' Can view Proyecto') >= 0):
            listaProyecto.append("view")

        if (permiso.find(' Can add Historia') >= 0):
            listaHistoria.append("add")
        if (permiso.find(' Can change Historia') >= 0):
            listaHistoria.append("change")
        if (permiso.find(' Can delete Historia') >= 0):
            listaHistoria.append("delete")
        if (permiso.find(' Can view Historia') >= 0):
            listaHistoria.append("view")

        if (permiso.find(' Can add sprint') >= 0):
            listaSprint.append("add")
        if (permiso.find(' Can change sprint') >= 0):
            listaSprint.append("change")
        if (permiso.find(' Can delete sprint') >= 0):
            listaSprint.append("delete")
        if (permiso.find(' Can view sprint') >= 0):
            listaSprint.append("view")

    request.session['Proyecto'] = listaProyecto
    request.session['Historia'] = listaHistoria
    request.session['Sprint'] = listaSprint



#VISTAS RELACIONADAS A SPRINTS
@login_required
@permission_required('Sprints.add_sprint', raise_exception=True)
def crearSprint(request):
    """
    Metodo para la creacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR PROYECTO
    """
    if request.method == "POST":
        formulario = crearSprintForm(request.POST,request=request.session)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosSprint=formulario.cleaned_data
            newSprint=nuevoSprint(datosSprint)
            return render(request, "outputCrearSprint.html", {"sprintCreado": datosSprint})
    else:
        usuarioActual = User.objects.get(username=request.user.username)
        if usuarioActual.proyecto_id is None:
            mensaje="Ustede no forma parte de ningun proyecto"
            return render(request, "Condicion_requerida.html",{"mensaje":mensaje})
        else:
            proy=model_to_dict(usuarioActual.proyecto)
            request.session['proyecto']=proy['id']
            sprintActualenProceso=sprintActivoen(proy['id'])
            #Si el proyecto no tiene todavia sprint o el sprint actual ya termino
            if(sprintActualenProceso == False):
                formulario = crearSprintForm(request=request.session)
                return render(request, "crearSprint.html", {"form": formulario})
            else:
                mensaje = "No puede crear un nuevo sprint hasta que el actual finalize"
                return render(request, "Condicion_requerida.html",{"mensaje":mensaje})
    return render(request, "crearSprint.html", {"form": formulario})

#MODIFICAR SPRINT
@login_required
@permission_required('Sprints.change_sprint', raise_exception=True)
def modificarSprint(request):
    """
    Metodo para la modificacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR PROYECTO
    """
    if request.method == "POST":
        formulario = modificarSprintForm(request.POST,request=request.session)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            #aca puede dar un problema con los datos de fechas
            datosSprint=formulario.cleaned_data

            fecha_fin=formulario.cleaned_data['fecha_fin']
            print('cleaned data = ',formulario.cleaned_data)
            updateSprint(formulario.cleaned_data)
            # Retornar mensaje de exito
            return render(request, "outputmodificarSprint.html", {"SprintModificado": datosSprint})
    else:
        usuarioActual = User.objects.get(username=request.user.username)
        if (usuarioActual.proyecto == None):
            return render(request, "Condicion_requerida.html")
        else:
            proyectoActual=usuarioActual.proyecto
            poseeSprintActivo=guardarCamposdeSprint(request,proyectoActual)
            if (poseeSprintActivo == True):
                formulario = modificarSprintForm(request=request.session)
                return render(request, "modificarSprint.html", {"form": formulario})
            else:
                mensaje = "No se puede modificar sprint ya que el proyecto aun no posee un sprint activo"
                return render(request, "Condicion_requerida.html", {"mensaje": mensaje})






##Solo muestra los sprint sin mayor detalle
@login_required
@permission_required('Sprints.view_sprint', raise_exception=True)
def visualizarSprint(request):
    """
    Metodo para la visualizacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de VISUALIZAR PROYECTO
    """
    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.proyecto == None):
        mensaje = "Usted no forma parte de ningun proyecto"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        proyectoActual=model_to_dict(usuarioActual.proyecto)
        listaSprint=proyectoActual['id_sprints']
        return render(request, "ListarSprints.html", {"Sprints": listaSprint})


@login_required
@permission_required('Sprints.view_sprint', raise_exception=True)
def visualizarSprint2(request,id):
    sprint=getSprint(id)
    sprint2 = model_to_dict(sprint)
    listaHistorias = sprint2['historias']
    cantidaddehistorias=len(listaHistorias)
    return render(request, "tableroKanbanSprintAnterior.html", {"Sprint": sprint, "Historias": listaHistorias,"Total":cantidaddehistorias})









##Esta vista es para mostrar el tablero kanban actual.
@login_required
def tableroKanban(request):
    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.proyecto == None):
        mensaje = "Usted no forma parte de ningun proyecto"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        proyectoActual = model_to_dict(usuarioActual.proyecto)
        listaSprint = proyectoActual['id_sprints']
        sprintActual=listaSprint[-1]
        sprintActual2=model_to_dict(sprintActual)
        listaHistorias=sprintActual2['historias']
        cantidaddehistorias = len(listaHistorias)
        return render(request, "tableroKanban.html", {"Sprint": sprintActual,"Historias": listaHistorias,"Total":cantidaddehistorias})





@login_required
def verMiembros(request):
    """
    Metodo que es ejecutado para mostrar los miembros de un proyecto

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de verMiembros
    """
    usuario = User.objects.get(username=request.user.username)
    id = usuario.proyecto_id
    usuarios = User.objects.filter(proyecto_id=id)
    fotos = {}

    for u in usuarios:
        fotos[u.email] = SocialAccount.objects.filter(user=u)[0].extra_data['picture']

    return render(request, "AvatarContent.html", {"miembros": usuarios, "fotos": fotos})


@login_required
@permission_required('userStory.add_historia', raise_exception=True)
def crearHistoria(request):
    """
    Metodo que es ejecutado para crear un user story

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de crearHistoria
    """
    if request.method == "POST":
        formulario = crearHistoriaForm(request.POST, proyecto=request.session['idproyecto'])
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosHistoria = formulario.cleaned_data
            print("el cleaned data en bruto del formulario de crear Historia")
            print(datosHistoria)

            datosHistoria['proyecto'] = getProyecto(formulario.cleaned_data['proyecto'])

            print("el cleaned data en bruto del formulario de crear Historia + asociado al proyecto actual")
            print(datosHistoria)

            nuevaHistoria(datosHistoria)

            # Retornar mensaje de exito
            return render(request, "outputCrearUserStory.html", {"historiaCreado": datosHistoria})
    else:
        usuarioActual = User.objects.get(username=request.user.username)
        u = model_to_dict(usuarioActual)
        request.session['idproyecto'] = u['proyecto']

        formulario = crearHistoriaForm(proyecto=request.session['idproyecto'])

    return render(request, "crearUserStory.html", {"form": formulario})


# Seleccionar historia 1
@login_required
@permission_required('userStory.add_historia', raise_exception=True)
def seleccionarHistoria(request):
    """
        Metodo para la asignacion de roles a los usuarios del sistema

        :param request: solicitud recibida
        :return: respuesta: a la solicitud de ASIGNAR ROL
    """
    if request.method == "POST":
        formulario = seleccionarHistoriaForm(request.POST, proyecto=request.session['idproyecto'])
        if (formulario.is_valid()):
            HistoriaSeleccionada = model_to_dict(formulario.cleaned_data['Historia'])
            print("el modelo de historia es:")
            print(HistoriaSeleccionada)

            request.session['HistoriaSeleccionada'] = HistoriaSeleccionada

            return redirect(modificarHistoria)
    else:
        usuarioActual = User.objects.get(username=request.user.username)
        usu = model_to_dict(usuarioActual)
        request.session['idproyecto'] = usu['proyecto']
        formulario = seleccionarHistoriaForm(proyecto=request.session['idproyecto'])
    return render(request, "seleccionarHistoria.html", {"form": formulario})


# modificar historia 2
@login_required
@permission_required('userStory.change_historia', raise_exception=True)
def modificarHistoria(request):
    """
        Metodo para la modificacion de proyectos

        :param request: solicitud recibida
        :return: respuesta a la solicitud de CREAR PROYECTO
    """
    if request.method == "POST":

        formulario = modificarHistoriaForm(request.POST, datosdelaHistoria=request.session['HistoriaSeleccionada'])
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosdeHistoria = formulario.cleaned_data
            print("Los datos del cleaned data son ahora")

            print(datosdeHistoria)
            # metodo que realiza la logica de la modificacion

            updateHistoria(datosdeHistoria)
            # Retornar mensaje de exito
            return render(request, "outputmodificarHistoria.html", {"historiaModificada": datosdeHistoria})
    else:

        formulario = modificarHistoriaForm(datosdelaHistoria=request.session['HistoriaSeleccionada'])

    return render(request, "modificarHistoria.html", {"form": formulario})

@login_required
@permission_required('userStory.delete_historia', raise_exception=True)
def eliminarHistoria(request):
    """
        Metodo para la asignacion de roles a los usuarios del sistema

        :param request: solicitud recibida
        :return: respuesta: a la solicitud de ASIGNAR ROL
    """
    if request.method == "POST":
        formulario = eliminarHistoriaForm(request.POST)
        if (formulario.is_valid()):
            HistoriaSeleccionado = formulario.cleaned_data['Historia']

            # Acciones a realizar con el form
            HistoriaSeleccionado.delete()
            # Retornar mensaje de exito
            return render(request, "outputEliminarHistoria.html", {"HistoriaEliminado": HistoriaSeleccionado})
    else:
        formulario = eliminarHistoriaForm()

    return render(request, "eliminarHistoria.html", {"form": formulario})

##testeo pendiente
@login_required
@permission_required('userStory.view_historia', raise_exception=True)
def verHistorias(request):
    """
    Metodo que es ejecutado para mostrar los miembros de un proyecto

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de verMiembros
    """
    id_proyectoActual = User.objects.get(username=request.user.username)
    id_proyectoActual = id_proyectoActual.proyecto_id
    historias = Historia.objects.filter(proyecto=id_proyectoActual)

    return render(request, "HistoriaContent.html", {"historias": historias})

#Esta es una vista que lista todas las historais del proyecto pero las que estarian dentro del product backlog
#es decir no estan en un sprint
@login_required
@permission_required('userStory.view_historia', raise_exception=True)
def productBacklog(request):
    """
    Metodo que es ejecutado para mostrar las historias del proyecto actual

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de verMiembros
    """
    id_proyectoActual = User.objects.get(username=request.user.username)
    id_proyectoActual = id_proyectoActual.proyecto_id
    historias = Historia.objects.filter(proyecto=id_proyectoActual,estados=None)

    return render(request, "HistoriaContent.html", {"historias": historias})


#Vista que hace la logica de cambio de estado en el kanban
@login_required
def moverHistoria(request,id,opcion):
    h=Historia.objects.get(id_historia=id)

    #print(f"Datos del formulario : {request.POST}")
    #print(f"Horas POST : {request.POST['horas']}")
    if request.method == 'POST':
        form = cargarHorasHistoriaForm(request.POST)
        print(f"form : {form}")
        if (form.is_valid()):
            horas = form.cleaned_data['horas']
            if horas > 0 :
                if (opcion == 5):
                    print(f"Historia con id {id} horas: {horas}")
                    h.horas_dedicadas = h.horas_dedicadas + horas
                    messages.success(request,"Horas registradas")
            else:
                messages.error(request, 'Ingrese una hora valida')
        else:
            print("formulario invalido")

    if (opcion==1):
        h.estados='PENDIENTE'
    if (opcion==2):
        h.estados='EN_CURSO'
        #Aca se debe agregar logica para asociar la histaria con el usuario.
    if (opcion==3):
        h.estados='FINALIZADO'
    if (opcion==4):
        h.estados='QUALITY_ASSURANCE'


    h.save()
    #aca se puede asociar una historia a un usuario
    #usuario = User.objects.get(username=request.user.username)
    #usuario.stories.add(h)

    return tableroKanban(request)


#vista que cambia el tiempo trabajado de un usuario

def lineChart(request):

    cal = Paraguay()
    #formatear fecha print(x.strftime("%b %d %Y %H:%M:%S"))
    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.proyecto == None):
        mensaje = "Usted no forma parte de ningun proyecto"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        proyectoActual = model_to_dict(usuarioActual.proyecto)
        listaSprint = proyectoActual['id_sprints']
        sprintActual=listaSprint[-1]
        sprintActual2=model_to_dict(sprintActual)
        listaHistorias=sprintActual2['historias']
        cantidaddehistorias = len(listaHistorias)

        #Obtener los dias laborales
        fechaInicio = sprintActual2['fecha_inicio']
        fechaFin = sprintActual2['fecha_fin']
        cantidadDias = cal.get_working_days_delta(fechaInicio, fechaFin)
        diasLaborales = []
        dias = []
        horasLaborales = []
        pasos = timedelta(days=1)
        print("calculando fechas")
        while fechaInicio <= fechaFin:
            if cal.is_working_day(fechaInicio):
                diasLaborales.append(fechaInicio)
                dias.append( fechaInicio.strftime("%d-%b"))
                print(fechaInicio)
            fechaInicio += pasos

        for i in range(cantidadDias):
            horasLaborales.append(5)

        print(diasLaborales)

        print("dias =",dias)
        print(cantidadDias)
        return render(request, "lineChart.html", {"Sprint": sprintActual,"Historias": listaHistorias,"Total":cantidaddehistorias,"diasLaborales":dias, "horasLaborales":horasLaborales, "cantidadDias":cantidadDias})

