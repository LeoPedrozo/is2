import requests
from django.forms import model_to_dict
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import date, datetime, timedelta
from workalendar.america import Paraguay
from django.db.models import Q
from django.http import HttpResponse
from django.db import models

from django.template import Template, Context
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from GestionPermisos.forms import crearRolForm, asignarRolForm, registroDeUsuariosForm, seleccionarRolForm, \
    modificarRolForm
from GestionPermisos.views import fabricarRol, enlazar_Usuario_con_Rol, registrar_usuario, removerRol
from Sprints.views import nuevoSprint, updateSprint, sprintActivoen, guardarCamposdeSprint, getSprint
from gestionUsuario.models import User, UserProyecto, UserSprint
from gestionUsuario.views import asociarProyectoaUsuario, desasociarUsuariodeProyecto
from is2.filters import UserFilter, HistoriaFilter, SprintFilter
from proyectos.views import nuevoProyecto, getProyecto, updateProyecto, guardarCamposdeProyecto
from proyectos.models import Proyecto
from proyectos.forms import crearproyectoForm, modificarproyectoForm, seleccionarProyectoForm, importarRolForm
from django.contrib.auth.decorators import user_passes_test
from Sprints.forms import crearSprintForm, modificarSprintForm, visualizarSprintForm, seleccionarSprintForm

from gestionUsuario.forms import asignarcapacidadForm
from Sprints.models import Sprint
from userStory.forms import crearHistoriaForm, seleccionarHistoriaForm, modificarHistoriaForm, eliminarHistoriaForm, \
    cargarHorasHistoriaForm, asignarEncargadoForm, asignarDesarrolladorForm
from userStory.models import Historia
from userStory.views import nuevaHistoria, updateHistoria, asignarEncargado
from django.conf import settings
from django.core.mail import send_mail

from django.core.exceptions import ObjectDoesNotExist


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
            usuario = User.objects.get(username=request.user.username)
            proyectos = usuario.proyectos_asociados.all()
            # proyecto=usuario.proyectos_asociados.first()
            # proyecto.
            return render(request, "sidenav.html",
                          {"avatar": None, "proyectoActual": usuario.proyecto, "proyectos": proyectos})
        else:
            usuario = User.objects.get(username=request.user.username)
            fotodeususario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']

            proyectos = usuario.proyectos_asociados.all()
            roles = ', '.join(map(str, usuario.groups.all()))
            return render(request, "sidenav.html",
                          {"avatar": fotodeususario, "proyectoActual": usuario.proyecto, "proyectos": proyectos,
                           "roles": roles})
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


def step1_CrearRol(request):
    """
        Metodo para la creacion de roles del sistema

        :param request: solicitud recibida
        :return: respuesta a la solicitud de CREAR ROL
        """
    if request.method == "POST":
        formulario = seleccionarProyectoForm(request.POST)
        if (formulario.is_valid()):
            datosRol = formulario.cleaned_data
            ProyectoSeleccionado = formulario.cleaned_data['Proyecto']
            request.session['ProyectoSeleccionado_id'] = ProyectoSeleccionado.id
            return redirect(step2_CrearRol)
    else:
        formulario = seleccionarProyectoForm()

    return render(request, "seleccionarProyecto.html", {"form": formulario})


@login_required
@permission_required('auth.add_group', raise_exception=True)
def step2_CrearRol(request):
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

            # Paso 1 Creamos el rol.

            fabricarRol(datosRol)

            # Paso 2 agregamos a la lista de proyecto
            idProyecto = request.session['ProyectoSeleccionado_id']
            proyectoseleccionado = Proyecto.objects.get(id=idProyecto)
            proyectoseleccionado.roles_name.append(nombreRol)
            proyectoseleccionado.save()

            # Retornar mensaje de exito
            return render(request, "rolCreado.html",
                          {"nombreRol": nombreRol, "historia": historia, "proyecto": proyecto, "sprint": sprint})
    else:
        formulario = crearRolForm()

    return render(request, "crearRol.html", {"form": formulario})


def step1_asignarRol(request):
    """
        Metodo para la creacion de roles del sistema

        :param request: solicitud recibida
        :return: respuesta a la solicitud de CREAR ROL
    """
    if request.method == "POST":
        formulario = seleccionarProyectoForm(request.POST)
        if (formulario.is_valid()):
            datosRol = formulario.cleaned_data
            ProyectoSeleccionado = formulario.cleaned_data['Proyecto']
            proyecto_dictionary = model_to_dict(ProyectoSeleccionado)
            request.session['id_proyecto'] = proyecto_dictionary['id']
            request.session['roles'] = proyecto_dictionary['roles_name']
            return redirect(step2_asignarRol)
    else:
        formulario = seleccionarProyectoForm()

    return render(request, "seleccionarProyecto.html", {"form": formulario})


@login_required
@permission_required('auth.add_group', raise_exception=True)
def step2_asignarRol(request):
    """
    Metodo para la asignacion de roles a los usuarios del sistema

    :param request: solicitud recibida
    :return: respuesta: a la solicitud de ASIGNAR ROL
    """
    if request.method == "POST":
        formulario = asignarRolForm(request.POST, proyecto=request.session)
        if (formulario.is_valid()):
            # Se estiran los datos del formulario
            datosRol = formulario.cleaned_data

            # user_object = formulario.cleaned_data['Usuario']
            user_name = formulario.cleaned_data['Usuario']
            rol_name = formulario.cleaned_data['Roles']

            # Realizo las consultas para tener el objeto Rol y el objeto proyecto para poder agregar en la tabla UserProy
            user_object = User.objects.get(username=user_name)
            rol_object = Group.objects.get(name=rol_name)
            proyecto_object = Proyecto.objects.get(id=request.session['id_proyecto'])

            # Teniendo los datos agrego el nuevo elemento a la tabla userproyecto
            # este if es para que no se agregue varios roles de un usuario para un mismo proyecto.

            if UserProyecto.objects.filter(usuario=user_object, proyecto=proyecto_object).exists():
                a = UserProyecto.objects.get(usuario=user_object, proyecto=proyecto_object)
                a.rol_name = rol_name
                a.save()
            else:
                nuevo = UserProyecto(usuario=user_object, proyecto=proyecto_object, rol_name=rol_name)
                nuevo.save()

            # Agrego al usuario al rol
            # Limpiar antiguo rol del usuario para el cambio
            # print("Limpiando antiguos roles")
            # user_object.groups.clear()
            # enlazar con el rol asignado para el proyecto
            enlazar_Usuario_con_Rol(user_object, rol_object)
            # registrar_usuario(user_object, 'True')
            # user_object.save()
            # Retornar mensaje de exito
            return render(request, "outputAsignarRol.html", {"asignaciondeRol": datosRol})
    else:
        procesoAsignarRol(request)
        formulario = asignarRolForm(proyecto=request.session)

    return render(request, "asignarRol.html", {"form": formulario})


# funcion que realiza la logica de preparar los datos para el formulario de asignar Rol
def procesoAsignarRol(request):
    # esto genera el formato adecuado para las opciones del formulario
    roles = []
    for rol in request.session['roles']:
        roles.append((rol, rol))
    # ----------------------------------------------------------------
    # Procedimiento para generar el queryset correcto para los usuarios.
    usuarios_names = []

    # users=UserProyecto.objects.filter(proyecto_id=request.session['id_proyecto'])
    p = Proyecto.objects.get(id=request.session['id_proyecto'])
    users = User.objects.filter(proyectos_asociados=p)
    for u in users:
        # usuarios_names.append( (u.usuario.username,u.usuario.username) )
        usuarios_names.append((u.username, u.username))

    request.session['usuario_names'] = usuarios_names
    request.session['roles_name'] = roles


# @login_required
# @permission_required('auth.delete_group', raise_exception=True)
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


def step1_eliminarRol(request):
    """
         Metodo para la creacion de roles del sistema

         :param request: solicitud recibida
         :return: respuesta a la solicitud de CREAR ROL
    """
    if request.method == "POST":
        formulario = seleccionarProyectoForm(request.POST)
        if (formulario.is_valid()):
            datosRol = formulario.cleaned_data
            ProyectoSeleccionado = formulario.cleaned_data['Proyecto']
            proyecto_dictionary = model_to_dict(ProyectoSeleccionado)
            request.session['id_proyecto'] = proyecto_dictionary['id']
            request.session['roles'] = proyecto_dictionary['roles_name']
            return redirect(step2_eliminarRol)
    else:
        formulario = seleccionarProyectoForm()
    return render(request, "seleccionarProyecto.html", {"form": formulario})


@login_required
@permission_required('auth.add_group', raise_exception=True)
def step2_eliminarRol(request):
    """
        Metodo para la asignacion de roles a los usuarios del sistema

        :param request: solicitud recibida
        :return: respuesta: a la solicitud de ASIGNAR ROL
    """
    if request.method == "POST":
        formulario = seleccionarRolForm(request.POST, proyecto=request.session)
        if (formulario.is_valid()):
            # 1 Se estira el dato del formulario
            RolSeleccionado = formulario.cleaned_data['Rol']
            # 2 Se consulta el objeto grupo

            # Estiramos el objeto proyecto
            proyecto = Proyecto.objects.get(id=request.session['id_proyecto'])
            # eliminamos de su lista el rol
            proyecto.roles_name.remove(RolSeleccionado)
            # eliminamos los registros que relacionan el rol con el usuario.
            UserProyecto.objects.filter(proyecto=proyecto, rol_name=RolSeleccionado).delete()
    else:
        # esto genera el formato adecuado para las opciones del formulario
        roles = []
        for rol in request.session['roles']:
            roles.append((rol, rol))
        # ---------------------------------------------------------------

        request.session['roles_name'] = roles
        formulario = seleccionarRolForm(proyecto=request.session)

    return render(request, "seleccionarRol.html", {"form": formulario})


def step1_modificarRol(request):
    """
         Metodo para la creacion de roles del sistema

         :param request: solicitud recibida
         :return: respuesta a la solicitud de CREAR ROL
    """
    if request.method == "POST":
        formulario = seleccionarProyectoForm(request.POST)
        if (formulario.is_valid()):
            datosRol = formulario.cleaned_data
            ProyectoSeleccionado = formulario.cleaned_data['Proyecto']
            proyecto_dictionary = model_to_dict(ProyectoSeleccionado)
            request.session['id_proyecto'] = proyecto_dictionary['id']
            request.session['roles'] = proyecto_dictionary['roles_name']
            return redirect(step2_modificarRol)
    else:
        formulario = seleccionarProyectoForm()
    return render(request, "seleccionarProyecto.html", {"form": formulario})


@login_required
@permission_required('auth.add_group', raise_exception=True)
def step2_modificarRol(request):
    """
        Metodo para la asignacion de roles a los usuarios del sistema

        :param request: solicitud recibida
        :return: respuesta: a la solicitud de ASIGNAR ROL
        """
    if request.method == "POST":
        formulario = seleccionarRolForm(request.POST, proyecto=request.session)
        if (formulario.is_valid()):
            # 1 Se estira el dato del formulario
            RolSeleccionado = formulario.cleaned_data['Rol']
            # 2 Se consulta el objeto grupo
            rol_object = Group.objects.get(name=RolSeleccionado)

            # 3 Pasamos el objeto a diccionario

            modeloRol = model_to_dict(rol_object)

            request.session['RolSeleccionado_id'] = modeloRol['id']

            print("En el paso 2 el id del rol es = ", modeloRol['id'])

            request.session['nombreRol'] = modeloRol['name']

            getPermisos(request, modeloRol['permissions'])

            return redirect(step3_modificarRol)
    else:
        # esto genera el formato adecuado para las opciones del formulario
        roles = []
        for rol in request.session['roles']:
            roles.append((rol, rol))
        # ---------------------------------------------------------------

        request.session['roles_name'] = roles
        formulario = seleccionarRolForm(proyecto=request.session)

    return render(request, "seleccionarRol.html", {"form": formulario})


# ESTE TIENE UN PROBLEMA, LA LISTA DE USUARIO SE MANTEIENE VACIA
# La linea 359 no funca. no da errores pero no hace lo que pienso.
@login_required
@permission_required('auth.change_group', raise_exception=True)
def step3_modificarRol(request):
    """
    Metodo para la modificacion de roles
    :param request: solicitud recibida
    :return: respuesta a la solicitud de MODIFICAR ROL
    """
    if request.method == "POST":

        formulario = modificarRolForm(request.POST, datosdelRol=request.session)
        if (formulario.is_valid()):
            # este dato es importante para la construccion del nuevor Rol con los nuevos permisos.
            datosNuevos = formulario.cleaned_data

            print("Los ajustes del nuevo Rol son = ", datosNuevos)

            # Obtener los usuarios que pertenecen al viejo rol, buscando por la id del rol
            viejoRol_id = request.session['RolSeleccionado_id']
            viejoRol_name = request.session['nombreRol']

            print("El id del Rol actualmente activo es = ", viejoRol_id, "y su nombre es = ", viejoRol_name)

            # Se estira los usuarios que forman parte al viejo Rol
            usuarios = User.objects.filter(groups__id=viejoRol_id)
            print("La lista de usuarios del rol viejo es = ", usuarios)

            # Objeto PRoyecto ok
            proyectoseleccionado = Proyecto.objects.get(id=request.session['id_proyecto'])
            # Se elimina el viejo Rol
            Group.objects.get(id=viejoRol_id).delete()

            # Se crea el nuevo Rol con sus respectivos permisos
            nombreRol = datosNuevos['RolName']
            # nuevoRol = fabricarRol(datosNuevos)
            fabricarRol(datosNuevos)

            nuevoRol = Group.objects.get(name=nombreRol)
            # Objeto PRoyecto
            # proyectoseleccionado = Proyecto.objects.get(id=request.session['id_proyecto'])
            # Este For es para actualizar la tabla de UserProyecto

            for usuario in usuarios:

                enlazar_Usuario_con_Rol(usuario, nuevoRol)
                print("Enlaza el usuario :", usuario, " con el nuevo rol ", nuevoRol)
                usuario_que_tieneRol = UserProyecto.objects.get(usuario=usuario, proyecto=proyectoseleccionado)
                if (usuario_que_tieneRol != None):  # si existe entra

                    usuario_que_tieneRol.rol_name = nombreRol
                    usuario_que_tieneRol.save()

            # Se debe eliminar el nombre del Rol de la lista de la tabla Proyecto.
            proyectoseleccionado.roles_name.remove(viejoRol_name)

            # Se debe agregar el nuevo rol al proyecto
            proyectoseleccionado.roles_name.append(nombreRol)
            proyectoseleccionado.save()

            # Retornar mensaje de exito
            return render(request, "outputmodificarRol.html", {"rolModificado": datosNuevos, "nombreRol": nombreRol})
    else:

        formulario = modificarRolForm(datosdelRol=request.session)

    return render(request, "modificarRol.html", {"form": formulario})


def importarRol(request):
    """
        Metodo para la creacion de roles del sistema

        :param request: solicitud recibida
        :return: respuesta a la solicitud de CREAR ROL
    """
    if request.method == "POST":
        formulario = importarRolForm(request.POST)
        if (formulario.is_valid()):
            datosRol = formulario.cleaned_data
            ProyectoOrigen = formulario.cleaned_data['ProyectoA']
            ProyectoDestino = formulario.cleaned_data['ProyectoB']

            diccionarioProyecto = model_to_dict(ProyectoOrigen)

            roles = ProyectoOrigen.roles_name
            # roles=diccionarioProyecto['roles_name']
            for rol in roles:
                ProyectoDestino.roles_name.append(rol)

            ProyectoDestino.save()
            return redirect(inicio)
    else:
        formulario = importarRolForm()
    # cambiar html
    return render(request, "seleccionarProyecto.html", {"form": formulario})


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
                return render(request, "outputmodificarProyecto.html",
                              {"proyectoCreado": datosProyecto, "members": miembrosActuales})
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
        messages.error(request, 'El usuario no posee ningun proyecto')
        return redirect(inicio)


@login_required
@permission_required('proyectos.delete_proyecto', raise_exception=True)
def eliminarProyecto(request):
    """
        Metodo para la eliminacion de proyectos

        :param request: solicitud recibida
        :return: respuesta: a la solicitud de ELIMINAR PROYECTO
    """
    if request.method == "POST":
        formulario = seleccionarProyectoForm(request.POST)
        if (formulario.is_valid()):
            ProyectoSeleccionado = formulario.cleaned_data['Proyecto']

            # eliminamos todas las historias asociadas a este proyecto
            id_proyecto = ProyectoSeleccionado.id
            Historia.objects.filter(proyecto=id_proyecto).delete()

            # eliminamos los sprints

            proyecto = model_to_dict(ProyectoSeleccionado)
            sprints = proyecto["id_sprints"]
            for s in sprints:
                s.delete()

            historias = Historia.objects.filter(proyecto=id_proyecto)
            for h in historias:
                h.delete()

            # desasociamos los ususarios del proyecto
            miembros = User.objects.filter(proyecto_id=id_proyecto).exclude(
                username='admin')

            # desasociamos proyecto con ususario
            desasociarUsuariodeProyecto(miembros)

            # Eliminamos proyecto
            ProyectoSeleccionado.delete()

            # Retornar mensaje de exito
            return render(request, "outputEliminarProyecto.html", {"Proyectoeliminado": ProyectoSeleccionado})
    else:
        formulario = seleccionarProyectoForm()

    return render(request, "eliminarProyecto.html", {"form": formulario})


# La logica de Roles aun no revisado.
def swichProyecto(request, id):
    u = User.objects.get(username=request.user.username)
    p = Proyecto.objects.get(id=id)
    u.proyecto = p

    if UserProyecto.objects.filter(usuario=u, proyecto=p).exists():
        print("Esta asociado al proyecto, reasignando rol...")
        proy = UserProyecto.objects.get(usuario=u, proyecto=p)
        rol_object = Group.objects.get(name=proy.rol_name)

        # Agrego al usuario al rol
        # Limpiar antiguo rol del usuario para el cambio
        print("Limpiando antiguos roles")
        u.groups.clear()
        # enlazar con el rol asignado para el proyecto
        enlazar_Usuario_con_Rol(u, rol_object)
        registrar_usuario(u, 'True')

    u.save()
    return redirect(inicio)


# ----------------------------------------------------
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


# VISTAS RELACIONADAS A SPRINTS
@login_required
@permission_required('Sprints.add_sprint', raise_exception=True)
def step1_SprintPlanning(request):
    """
    Metodo para la creacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR PROYECTO
    """
    if request.method == "POST":
        formulario = crearSprintForm(request.POST, request=request.session)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosSprint = formulario.cleaned_data
            print("SE CREA EL SPRINT")
            newSprint = nuevoSprint(datosSprint)

            # Por practicidad se le pasa el id del sprint
            request.session['sprint_planning_id'] = newSprint.id
            # return render(request, "outputCrearSprint.html", {"sprintCreado": datosSprint})
            print("REDIRECT PAPU")
            return redirect(step2_SprintPlanning)

    else:
        usuarioActual = User.objects.get(username=request.user.username)
        if usuarioActual.proyecto_id is None:
            mensaje = "Ustede no forma parte de ningun proyecto"
            return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
        else:
            proy = usuarioActual.proyecto.id
            request.session['proyecto'] = proy

            formulario = crearSprintForm(request=request.session)
            return render(request, "SprintPlanning_1.html", {"form": formulario})

    return render(request, "SprintPlanning_1.html", {"form": formulario})


def step2_SprintPlanning(request):
    """
        Metodo que es ejecutado para mostrar los miembros de un proyecto

        :param request: consulta recibida
        :return: respuesta a la solicitud de ejecucion de verMiembros
    """
    proyecto_actual = Proyecto.objects.get(id=request.session['proyecto'])
    sprint_actual = Sprint.objects.get(id=request.session['sprint_planning_id'])
    usuarios = []
    # aca en este filter se puede agregar la condicion de que tengan el rol de developer.
    # tablaparcial tiene la lista de usuarios del proyecto,<sin filtrar>
    PosiblesIntegrantes = UserProyecto.objects.filter(proyecto=proyecto_actual, rol_name="Desarrollador")

    print("La lista de posibles integrantes son :", PosiblesIntegrantes)
    # tablaparcial2=UserSprint.objects.filter(proyecto=proyecto_actual,sprint=sprint_actual)

    # este for es para poder generar la lista de usuarios que se pueden seleccionar
    for elemento in PosiblesIntegrantes:

        u = UserSprint.objects.filter(proyecto=proyecto_actual, usuario=elemento.usuario, sprint=sprint_actual)
        print("existe -> ", u)
        # si el usuario ya existe en la tabla entonces no hace falta agregar 2 veces. No entra en el if
        if (len(u) == 0):
            print("El usuario ", elemento.usuario.username, " es agregado a la lista")
            usuarios.append(elemento.usuario)

    return render(request, "SprintPlanning_2.html", {"miembros": usuarios})


def asignarCapacidad(request, id):
    if request.method == 'POST':
        form = asignarcapacidadForm(request.POST)
        print(f"form : {form}")
        if (form.is_valid()):
            capacidad = form.cleaned_data['capacidad']
            print("LA CAPACIDAD ES : ", capacidad)
            if capacidad > 0:
                print("Entro en el prime if")
                usuario=User.objects.get(id=id)
                proyecto_actual=Proyecto.objects.get(id=request.session['proyecto'])
                sprint_en_planning=Sprint.objects.get(id=request.session['sprint_planning_id'])

                try:
                    u = UserSprint.objects.get(usuario=usuario, proyecto=proyecto_actual, sprint=sprint_en_planning)
                except ObjectDoesNotExist:
                    nuevoElemento = UserSprint(usuario=usuario, proyecto=proyecto_actual, sprint=sprint_en_planning,
                                               capacidad=capacidad)
                    nuevoElemento.save()
                else:

                    u.capacidad = capacidad
                    u.save()

            else:
                messages.error(request, 'Ingrese una capacidad valida')
        else:
            print("formulario invalido")

    return redirect(step2_SprintPlanning)


def step3_SprintPlanning(request):
    """
        Metodo para visualizar el tablero kanban

        :param request: solicitud recibida
        :return: respuesta a la solicitud de TABLERO KANBAN
    """

    proyectoActual = Proyecto.objects.get(id=request.session['proyecto'])
    sprintActual = Sprint.objects.get(id=request.session['sprint_planning_id'])

    # Lista 1 y 2 son las historias del proyecto y del sprint actualmente
    Lista1 = Historia.objects.filter(proyecto=proyectoActual)
    Lista2 = sprintActual.historias.all()
    prioridades = ["ALTA", "MEDIA", "BAJA"]

    # Como no estan ordenadas creamos otras listas que son ordenadas
    productbacklog = []
    sprintbacklog = []

    # ordenamos la lista Alta Media Baja
    for p in prioridades:
        for h in Lista1:
            if h.prioridad == p:
                productbacklog.append(h)

    for p in prioridades:
        for h in Lista2:
            if h.prioridad == p:
                sprintbacklog.append(h)

    tablatemporal = UserSprint.objects.filter(proyecto=proyectoActual, sprint=sprintActual)
    developers = []

    # La lista de los desarrolladores para el sprint actual
    for elemento in tablatemporal:
        developers.append((elemento.usuario.username, elemento.usuario.username))

    cantidaddehistorias = len(productbacklog)

    request.session['developers'] = developers
    # Formulario para el selector de usuarios
    formulario = asignarDesarrolladorForm(developers=request.session)

    return render(request, "SprintPlanning_3.html", {"Sprint": sprintActual, "p_backlog": productbacklog,
                                                     "s_backlog": sprintbacklog, "Total": cantidaddehistorias,
                                                     "form": formulario})


# No funciona con redirect aunque con ese seria mejor.
def step3_asignarEncargado(request, id, opcion):
    # h = Historia.objects.get(id_historia=id)
    sprint_actual = Sprint.objects.get(id=request.session['sprint_planning_id'])

    if (opcion == 1):
        h = Historia.objects.get(id_historia=id)
        if request.method == 'POST':
            formulario = asignarDesarrolladorForm(request.POST, developers=request.session)
            if (formulario.is_valid()):
                usuarioSeleccionado = formulario.cleaned_data['encargado']
                encargado = User.objects.get(username=usuarioSeleccionado)
                h.encargado = encargado
                h.estados = 'PENDIENTE'
                h.save()
                # Se le agrega al sprint
                sprint_actual.historias.add(h)
                sprint_actual.save()
            else:
                print("formulario invalido")

    if (opcion == 2):
        h = Historia.objects.get(id_historia=id)
        h.encargado = None
        h.estados = ""
        h.save()
        sprint_actual.historias.remove(h)
        sprint_actual.save()

    # Iniciar
    if (opcion == 3):
        print('el sprint actual tiene el estado = ', sprint_actual.estados)
        u = UserSprint.objects.filter(sprint=sprint_actual).first()
        listasprints = u.proyecto.id_sprints
        if (not listasprints.filter(estados="INICIADO").exists()):
            sprint_actual.estados = 'INICIADO'
            sprint_actual.save()
            return redirect(tableroKanban)
        else:
            mensaje = "No puede iniciar Otro sprint ya que esta uno actualmente en progreso"
            return render(request, "Condicion_requerida.html", {"mensaje": mensaje})

    # guardar
    if (opcion == 4):
        sprint_actual.estados = 'PLANNING'
        sprint_actual.save()
        # redireccionar a lista de sprints
        return redirect(visualizarSprint)

    return redirect(step3_SprintPlanning)
    # return step3_SprintPlanning(request)


# Esta vista va a estar en lista de sprints
# MODIFICAR SPRINT

@login_required
@permission_required('Sprints.change_sprint', raise_exception=True)
def modificarSprint(request, id_sprint):
    """
    Metodo para la modificacion de sprint

    :param request: solicitud recibida
    :return: respuesta a la solicitud de MODIFICAR SPRINT
    """
    if request.method == "POST":
        formulario = modificarSprintForm(request.POST, request=request.session)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            # aca puede dar un problema con los datos de fechas
            datosSprint = formulario.cleaned_data
            updated_sprint = updateSprint(formulario.cleaned_data)
            # Por practicidad se le pasa el id del sprint
            request.session['sprint_planning_id'] = updated_sprint.id
            return redirect(step2_SprintPlanning)
    else:
        sprint_seleccionado = Sprint.objects.get(id=id_sprint)
        u = UserSprint.objects.filter(sprint=sprint_seleccionado)
        proyectoPropietario = u.first().proyecto
        request.session['proyecto'] = proyectoPropietario.id
        guardarCamposdeSprint(request, sprint_seleccionado, proyectoPropietario.id)
        formulario = modificarSprintForm(request=request.session)
        return render(request, "modificarSprint.html", {"form": formulario})


def eliminarSprint(request, id_sprint):
    sprint_seleccionado = Sprint.objects.get(id=id_sprint)

    # eliminamos la informacion relacionada al sprint de la tabla UserSprint
    UserSprint.objects.filter(sprint=sprint_seleccionado).delete()
    # Eliminamos el sprint del proyecto
    # u = UserSprint.objects.filter(sprint=sprint_seleccionado)
    # proyectoPropietario = u.first()
    # proyectoPropietario= proyectoPropietario.proyecto
    # proyectoPropietario.id_sprints

    #
    historias = sprint_seleccionado.historias.all()
    for h in historias:
        h.encargado = None
        h.estados = ""
        h.save()

    sprint_seleccionado.delete()

    return redirect(visualizarSprint)


##Solo muestra los sprint sin mayor detalle
@login_required
@permission_required('Sprints.view_sprint', raise_exception=True)
def visualizarSprint(request):
    """
    Metodo para la visualizacion de Sprints

    :param request: solicitud recibida
    :return: respuesta a la solicitud de VISUALIZAR SPRINT
    """
    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.proyecto == None):
        mensaje = "Usted no forma parte de ningun proyecto"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        proyectoActual = model_to_dict(usuarioActual.proyecto)
        listaSprint = proyectoActual['id_sprints']
        return render(request, "ListarSprints.html", {"Sprints": listaSprint})


@login_required
@permission_required('Sprints.view_sprint', raise_exception=True)
def visualizarSprint2(request, id):
    sprint = getSprint(id)
    sprint2 = model_to_dict(sprint)
    listaHistorias = sprint2['historias']
    cantidaddehistorias = len(listaHistorias)
    enFecha = sprint2['fecha_fin']
    fecha = datetime(enFecha.year, enFecha.month, enFecha.day, 23, 59, 59)
    # print(fecha)
    hists = []
    for historia in listaHistorias:
        hists.append(historia.history.as_of(fecha))

    return render(request, "tableroKanbanSprintAnterior.html",
                  {"Sprint": sprint, "Historias": hists, "Total": cantidaddehistorias})


##Esta vista es para mostrar el tablero kanban actual.
@login_required
def tableroKanban(request, opcion=''):
    """
    Metodo para visualizar el tablero kanban

    :param request: solicitud recibida
    :return: respuesta a la solicitud de TABLERO KANBAN
    """
    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.proyecto == None):
        mensaje = "Usted no forma parte de ningun proyecto"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        # proyectoActual = model_to_dict(usuarioActual.proyecto)
        # listaSprint = proyectoActual['id_sprints']
        proyectoActual = usuarioActual.proyecto
        sprintActual = proyectoActual.id_sprints.get(estados="INICIADO")
        try:
            # sprintActual = listaSprint[-1]

            sprintActual2 = model_to_dict(sprintActual)
            listaHistorias = sprintActual2['historias']

            versionesDic = {}
            for hist in listaHistorias:
                x = hist.history.filter(Q(estados='EN_CURSO') & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                    history_date__lte=sprintActual2['fecha_fin']))
                print("Historias",x)
                listaDeComentarios = []
                for z in list(x):
                    fech = z.history_date
                    fechaComentario = fech.strftime("%d-%b-%Y : ") + z.comentarios
                    if not fechaComentario in listaDeComentarios:
                        listaDeComentarios.append(fechaComentario)

                versionesDic[hist.id_historia] = listaDeComentarios
            print(versionesDic)
            cantidaddehistorias = len(listaHistorias)

            if not opcion == '':
                grupos = ', '.join(map(str, usuarioActual.groups.all()))
                print("grupos del usuario = ", grupos)
                try:
                    if grupos.find('Scrum Master'):
                        messages.info(request, "Finalizando Sprint")
                        #Marcar el ultimo estado que tenian las historias
                        for hist in listaHistorias:
                            hist._change_reason = 'fin_sprint'
                            hist.save()
                        #Ahora que ya se tiene el ultimo estado, procedemos a finalizar
                        for hist in listaHistorias:
                            if hist.estados == 'FINALIZADO':
                                hist.estados = 'QUALITY_ASSURANCE'
                            else:
                                hist.estados = ''
                                hist.encargado = None
                            hist.save()
                    sprintActual.estados = 'FINALIZADO'
                    sprintActual.save()
                except TypeError:
                    messages.error(request, "Debes ser Scrum")
            return render(request, "tableroKanban.html",
                      {"Sprint": sprintActual, "Historias": listaHistorias, "Total": cantidaddehistorias,
                       "versionesDic": versionesDic})
        except IndexError:
            return render(request, "Condicion_requerida.html", {"mensaje": "NO TIENE NINGUN SPRINT"})


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
    Metodo para la modificacion de historia, primeramente es necesario seleccionar la historia a ser modificada

    :param request: solicitud recibida
    :return: respuesta: a la solicitud de SELECCIONAR HISTORIA
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


# Seleccionar historia 1
@login_required
@permission_required('Sprints.add_sprint', raise_exception=True)
def asignarHistoriaEncargado(request):
    """
    Metodo para la asignacion de una historia a un usuario como encargado

    :param request: solicitud recibida
    :return: respuesta: a la solicitud de Asignar Encargado
    """
    if request.method == "POST":
        formulario = asignarEncargadoForm(request.POST)
        if (formulario.is_valid()):
            Historias = formulario.cleaned_data['Historia']
            usuarioEncargado = formulario.cleaned_data['Usuario']
            print("el modelo de historia es:")
            print(Historias)
            print("El encargado de la historia : ", usuarioEncargado)
            asignarEncargado(Historias, usuarioEncargado)
            return render(request, "outputasignarEncargado.html",
                          {"historias": Historias, "encargado": usuarioEncargado})
    else:
        formulario = asignarEncargadoForm(request.POST)
    return render(request, "asignarEncargado.html", {"form": formulario})


# modificar historia 2
@login_required
@permission_required('userStory.change_historia', raise_exception=True)
def modificarHistoria(request):
    """
    Metodo para la modificacion de historias

    :param request: solicitud recibida
    :return: respuesta a la solicitud de MODIFICAR HISTORIA
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
    Metodo para eliminar historias

    :param request: solicitud recibida
    :return: respuesta: a la solicitud de ELIMINAR HISTORIA
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
    Metodo que es ejecutado para mostrar las historias de usuario

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de verHistorias
    """
    id_proyectoActual = User.objects.get(username=request.user.username)
    id_proyectoActual = id_proyectoActual.proyecto_id
    historias = Historia.objects.filter(proyecto=id_proyectoActual)

    return render(request, "HistoriaContent.html", {"historias": historias})


# Esta es una vista que lista todas las historais del proyecto pero las que estarian dentro del product backlog
# es decir no estan en un sprint
@login_required
@permission_required('userStory.view_historia', raise_exception=True)
def productBacklog(request):
    """
    Metodo que es ejecutado para mostrar el Product Backlog

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de PRODUCT BACKLOG
    """
    id_proyectoActual = User.objects.get(username=request.user.username)
    id_proyectoActual = id_proyectoActual.proyecto_id
    historias = Historia.objects.filter(proyecto=id_proyectoActual, estados="")

    return render(request, "HistoriaContent.html", {"historias": historias})


# Vista que hace la logica de cambio de estado en el kanban
@login_required
def moverHistoria(request, id, opcion):
    """
    Metodo para administrar el cambio de estado de historias en el tablero kanban

    :param request: solicitud recibida
    :param id: identificador de la historia a mover
    :param opcion: estado de la historia
    :return: tablero kanban actualizado
    """
    h = Historia.objects.get(id_historia=id)
    encargado = User.objects.get(username=request.user.username)
    # Agregar Tiempo
    if request.method == 'POST':
        form = cargarHorasHistoriaForm(request.POST)
        print(f"form : {form}")
        if (form.is_valid()):
            horas = form.cleaned_data['horas']
            comentario = form.cleaned_data['comentario']
            if horas > 0:
                print("Usuario que solicita : ", request.user)
                print("Encargado : ", h.encargado)
                if request.user == h.encargado:
                    if (opcion == 5):
                        print(f"Historia con id {id} horas: {horas}, comentario: {comentario}")
                        h.horas_dedicadas = h.horas_dedicadas + horas
                        h.comentarios = comentario
                        messages.success(request, "Horas registradas")
                else:
                    messages.error(request, "No eres el encargado de la historia")
                    messages.info(request, f"El encargado es {h.encargado}")
            else:
                messages.error(request, 'Ingrese una hora valida')
        else:
            print("formulario invalido")

    if (opcion == 1):
        if (h.encargado == encargado):
            h.estados = 'PENDIENTE'
            messages.success(request, "Pasado a pendiente")
        else:
            messages.error(request, "No eres el encargado de la historia")

    if (opcion == 2):
        if (h.encargado == encargado):
            h.estados = 'EN_CURSO'
            messages.success(request, "Pasado a en curso")
        else:
            messages.error(request, "No eres el encargado de la historia")

    if (opcion == 3):
        if (h.encargado == encargado):
            h.estados = 'FINALIZADO'
            messages.success(request, "Finalizado")
        else:
            messages.error(request, "No eres el encargado de la historia")

    h.save()
    # aca se puede asociar una historia a un usuario
    # usuario = User.objects.get(username=request.user.username)
    # usuario.stories.add(h)

    return tableroKanban(request)


def asignarSprint(request, id):
    # 1 cambiamos el estado de la historia a agregar a
    """
    Metodo para asignar Sprint a una historia

    :param request: solicitud recibida
    :param id: identificador de la historia
    :return: sprint agregado a la historia
    """
    h = Historia.objects.get(id_historia=id)
    h.estados = 'PENDIENTE'
    h.save()
    # 2 tenemos que agregar la historia al sprint
    id_proyectoActual = User.objects.get(username=request.user.username)
    proyecto = id_proyectoActual.proyecto
    sprintActual = proyecto.id_sprints.last()

    try:
        sprintActual.historias.add(h)
        proyecto.save()

        messages.success(request, "Operacion realizada con exito")
        return search(request)
    except AttributeError:
        messages.error(request, "No posee sprints")
        return search(request)


# vista que cambia el tiempo trabajado de un usuario
def lineChart(request):
    """
    Metodo para Graficar el burndown chart en un gráfico de linea

    :param request: solicitud recibida
    :return: grafico de burndown chart
    """
    cal = Paraguay()
    # formatear fecha print(x.strftime("%b %d %Y %H:%M:%S"))
    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.proyecto == None):
        mensaje = "Usted no forma parte de ningun proyecto"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        proyectoActual = model_to_dict(usuarioActual.proyecto)
        listaSprint = proyectoActual['id_sprints']
        sprintActual = listaSprint[-1]

        sprintActual2 = model_to_dict(sprintActual)
        listaHistorias = sprintActual2['historias']
        cantidaddehistorias = len(listaHistorias)

        # Los miembros en forma de cadena para saber su estado
        miembrosSprint = []
        for hist in listaHistorias:
            try:
                lastlog = hist.encargado.last_login.strftime("%d/%b - %I:%M %p")
                miembrosSprint.append(f"{hist.encargado.email}\nUlt. activo : {lastlog}")
            except AttributeError:
                print(f"la historia {hist} aun no tiene encargado")
        fechaInicio = sprintActual2['fecha_inicio']
        fechaFin = sprintActual2['fecha_fin']
        cantidadDias = cal.get_working_days_delta(fechaInicio, fechaFin) + 1

        # variables a las cuales depende el line-chart
        diasLaborales = []
        dias = []
        horasLaboralesIdeal = []
        horasLaboralesReal = []
        pasos = timedelta(days=1)

        print("calculando fechas")
        while fechaInicio <= fechaFin:
            if cal.is_working_day(fechaInicio):
                diasLaborales.append(fechaInicio)
                dias.append(fechaInicio.strftime("%d-%b"))
                print(fechaInicio)
            fechaInicio += pasos

        # Esto lo agregue por que estoy re loco
        ideal = sprintActual2["horasLaboralesIdeal"]
        # real = sprintActual2["horasLaboralesReal"]

        calcularEsfuerzoDiario(listaHistorias, sprintActual, dias)
        real = formatearlista(sprintActual.horasLaboralesReal)

        total = 0
        for h in listaHistorias:
            total = total + (h.horasEstimadas)

        k = total / cantidadDias

        for i in range(cantidadDias):
            horasLaboralesIdeal.append(str(total))
            total = total - k;

        return render(request, "lineChart.html",
                      {"Sprint": sprintActual, "Historias": listaHistorias, "Total": cantidaddehistorias,
                       "diasLaborales": ','.join(dias), "horasLaboralesIdeal": ','.join(horasLaboralesIdeal),
                       "horasLaboralesReal": ','.join(real), "cantidadDias": cantidadDias, "miembros": miembrosSprint})


def calcularEsfuerzoDiario(Historias, sprint, Dias):
    """
    Metodo para obtener el esfuerzo diario en las historias de usuario, necesario para graficar el burndown chart

    :param Historias: Lista de Historias
    :param sprint: Sprint actual
    :param Dias: Dia actual
    :return: void
    """
    # FASE 1
    # Calcula el esfuerzo total del dia
    esfuerzoDiario = 0
    for historia in Historias:
        esfuerzoDiario = esfuerzoDiario + (historia.horasEstimadas - historia.horas_dedicadas)
    # -------------------------------

    # FASE 2
    # Se agrega a el esfuerzo a la lista
    hoy = datetime.today()
    hoy = hoy + timedelta(days=2)
    hoy = hoy.strftime("%d-%b")
    if (hoy in Dias):
        posicionEquivalenteDia = Dias.index(hoy)

        print("Posicion : ", posicionEquivalenteDia)
        print("Longitud : ", len(sprint.horasLaboralesReal))

        if (len(sprint.horasLaboralesReal) == 0):
            sprint.horasLaboralesReal.insert(posicionEquivalenteDia, esfuerzoDiario)
        else:
            try:
                sprint.horasLaboralesReal.insert(posicionEquivalenteDia, esfuerzoDiario)
                sprint.horasLaboralesReal.pop(posicionEquivalenteDia + 1)
            except IndexError:
                print("posicionEquivalenteDia+1 no existia")
                # sprint.horasLaboralesReal.insert(posicionEquivalenteDia, esfuerzoDiario)
                # sprint.horasLaboralesReal.pop(posicionEquivalenteDia + 1)

        sprint.save()


def formatearlista(lista):
    listaStrings = []

    for i in lista:
        listaStrings.append(str(i))

    return listaStrings


def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)

    id_proyectoActual = User.objects.get(username=request.user.username)
    id_proyectoActual = id_proyectoActual.proyecto_id
    historias = Historia.objects.filter(proyecto=id_proyectoActual)
    historia_list = Historia.objects.all()
    historia_filter = HistoriaFilter(request.GET, queryset=historia_list)
    return render(request, 'product_backlog.html', {'filter': historia_filter})


@login_required
def tableroQA_Release(request):
    """
    Metodo para visualizar el tablero Quality Assurance Release

    :param request: solicitud recibida
    :return: respuesta a la solicitud de TABLERO-QA RELEASE
    """
    print(f"id={id}")

    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.proyecto == None):
        mensaje = "Usted no forma parte de ningun proyecto"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        proyectoActual = model_to_dict(usuarioActual.proyecto)
        listaSprint = proyectoActual['id_sprints']

        #Primero se obtiene la lista de los sprints no verificados que hayan finalizado
        sprintsNoVerificados = []
        for sprint in listaSprint:
            if (not sprint.verificado) and sprint.estados == 'FINALIZADO':
                sprintsNoVerificados.append((sprint.id,sprint.sprintNumber))

        print(sprintsNoVerificados)
        if not sprintsNoVerificados:
            messages.error(request, "No hay ningun sprint finalizado")
        #desplegar selector
        messages.info(request,"seleccione un Sprint")
        if request.method == "POST":
            formulario = seleccionarSprintForm(request.POST, listaSprint=sprintsNoVerificados)
            if (formulario.is_valid()):
                sprintSeleccionado = formulario.cleaned_data['sprint']
        else:
            formulario = seleccionarSprintForm(listaSprint=sprintsNoVerificados)
            return render(request, "QA_sprint.html", {"form": formulario})

        try:
            print("Sprint seleccionado : ",sprintSeleccionado)
            sprintActual = Sprint.objects.get(id=sprintSeleccionado)
            sprintActual2 = model_to_dict(sprintActual)
            listaHistorias = sprintActual2['historias']
            versionesDic = {}
            for hist in listaHistorias:
                x=hist.history.filter(Q(estados='FINALIZADO') & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(history_date__lte=sprintActual2['fecha_fin']))
                listaDeComentarios=[]
                for z in list(x):
                    fech = z.history_date
                    fechaComentario=fech.strftime("%d-%b-%Y : ")+z.comentarios
                    if not fechaComentario in listaDeComentarios:
                        listaDeComentarios.append(fechaComentario)

                versionesDic[hist.id_historia] = listaDeComentarios
               # print(versionesDic)
            cantidaddehistorias = len(listaHistorias)
            print(listaHistorias)
            return render(request, "QA_sprint.html",{"Sprint": sprintActual2, "Historias": listaHistorias, "Total": cantidaddehistorias, "versionesDic":versionesDic})
        except IndexError:
            return render(request, "Condicion_requerida.html", {"mensaje":"NINGUNA HISRORIA PARA HACER QA"})
        except UnboundLocalError:
            return render(request, "Condicion_requerida.html", {"mensaje": "NO HAY SPRINTS PARA SELECCIONAR"})

# Vista que hace la logica de cambio de estado en el kanban
@login_required
def moverHistoriaQA(request, id, opcion):
    """
    Metodo para administrar el cambio de estado de historias en el tablero kanban

    :param request: solicitud recibida
    :param id: identificador de la historia a mover
    :param opcion: estado de la historia
    :return: tablero kanban actualizado
    """
    h = Historia.objects.get(id_historia=id)
    encargado=User.objects.get(username=request.user.username)

    #aceptar en quality assurance la historia, entonces va a pasar a Release
    if (opcion == 6):
        h.estados = 'RELEASE'
        messages.info(request, "Historia enviada a Release")
    #Rechazar la historia, vuelve al Product backlog pero con prioridad aumentada
    if (opcion == 7):
        h.estados = ""
        if h.prioridad == 'BAJA':
            h.prioridad = 'MEDIA'
        else:
            h.prioridad = 'ALTA'
        messages.info(request, "Historia rechazada")
        messages.info(request, f"Nueva prioridad {h.prioridad}")
    print("Historia : ",h)
    h.save()
    # aca se puede asociar una historia a un usuario
    # usuario = User.objects.get(username=request.user.username)
    # usuario.stories.add(h)

    return tableroQA_Release(request)

##Solo muestra los sprint sin mayor detalle
@login_required
@permission_required('Sprints.view_sprint', raise_exception=True)
def visualizarSprintFilter(request):
    """
    Metodo para la visualizacion de Sprints

    :param request: solicitud recibida
    :return: respuesta a la solicitud de VISUALIZAR SPRINT
    """
    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.proyecto == None):
        mensaje = "Usted no forma parte de ningun proyecto"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        #proyectoActual = model_to_dict(usuarioActual.proyecto)

        proyectoActual =usuarioActual.proyecto
        listaSprint=proyectoActual.id_sprints.all()
        #listaSprint = proyectoActual['id_sprints']
        sprint_filter = SprintFilter(request.GET, queryset=listaSprint)
        return render(request, "historialSprint.html", {"Sprints": listaSprint,'filter': sprint_filter})