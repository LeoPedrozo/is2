import requests
from django.forms import model_to_dict
from django.contrib.auth.models import Group
from django.contrib import messages

from django.http import HttpResponse
from django.db import models

from django.template import Template, Context
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from GestionPermisos.forms import crearRolForm, asignarRolForm, registroDeUsuariosForm, seleccionarRolForm, \
    modificarRolForm
from GestionPermisos.views import fabricarRol, enlazar_Usuario_con_Rol, registrar_usuario, removerRol
from Sprints.views import nuevoSprint,updateSprint,sprintActivoen,guardarCamposdeSprint
from gestionUsuario.models import User
from gestionUsuario.views import asociarProyectoaUsuario, desasociarUsuariodeProyecto
from proyectos.views import nuevoProyecto, getProyecto, updateProyecto,guardarCamposdeProyecto
from proyectos.forms import crearproyectoForm, modificarproyectoForm, eliminarProyectoForm
from proyectos.models import Proyecto
from proyectos.forms import crearproyectoForm, modificarproyectoForm,eliminarProyectoForm
from django.contrib.auth.decorators import user_passes_test
from Sprints.forms import crearSprintForm, modificarSprintForm, visualizarSprintForm
from userStory.forms import crearHistoriaForm, seleccionarHistoriaForm, modificarHistoriaForm, eliminarHistoriaForm
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

    return render(request, "modificarProyecto.html", {"form": formulario})


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


##No se deberia guardar la configuracion de proyecto?
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

            # Acciones a realizar con el form
            ProyectoSeleccionado.delete()
            # Retornar mensaje de exito
            return render(request, "outputEliminarProyecto.html", {"Proyectoeliminado": ProyectoSeleccionado})
    else:
        formulario = eliminarProyectoForm()

    return render(request, "eliminarProyecto.html", {"form": formulario})


##Metodo bastante horrible pero que hace su funcion.
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

        #Si no pertence a un proyecto

        print("usuarioActual.proyecto_id = ",usuarioActual.proyecto_id)
        print("usuarioActual.proyecto = ", usuarioActual.proyecto)


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


#MODIFICAR SPRINT
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
            guardarCamposdeSprint(request,proyectoActual)
            formulario = modificarSprintForm(request=request.session)
            return render(request, "modificarSprint.html", {"form": formulario})


##Solo muestra los sprint sin mayor detalle
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


##Falta funcionalidad de cambiar de estado
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

        return render(request, "tableroKanban.html", {"Sprint": sprintActual,"Historias": listaHistorias})




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
def productBacklog(request):
    """
    Metodo que es ejecutado para mostrar los miembros de un proyecto

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de verMiembros
    """
    id_proyectoActual = User.objects.get(username=request.user.username)
    id_proyectoActual = id_proyectoActual.proyecto_id
    historias = Historia.objects.filter(proyecto=id_proyectoActual,estados=None)

    return render(request, "HistoriaContent.html", {"historias": historias})