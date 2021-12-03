from datetime import date, datetime, timedelta
from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from workalendar.america import Paraguay
from GestionPermisos.forms import crearRolForm, asignarRolForm, registroDeUsuariosForm, seleccionarRolForm,modificarRolForm
from GestionPermisos.views import fabricarRol, enlazar_Usuario_con_Rol, registrar_usuario, removerRol
from Sprints.forms import crearSprintForm, modificarSprintForm, seleccionarSprintForm, extenderSprintForm,intercambiardeveloperForm
from Sprints.models import Sprint
from Sprints.views import nuevoSprint, updateSprint, guardarCamposdeSprint, getSprint
from gestionUsuario.forms import asignarcapacidadForm
from gestionUsuario.models import User, UserProyecto, UserSprint
from gestionUsuario.views import asociarProyectoaUsuario, desasociarUsuariodeProyecto
from is2.emails import email_rolAsignado, email_nuevoProyecto, email_historiaAsignado, email_actividadEnKanban, \
    email_actividadEnQA, email_nuevoSprint, email_sprintExtFin, email_proyectoFin, email_proyectoIni, \
    email_sprintCreado, email_sprintIniciado, email_sprintFinalizado, sprintVerificado, email_excluidoDelProyecto
from is2.filters import UserFilter, HistoriaFilter, SprintFilter, ProyectoFilter
from proyectos.forms import crearproyectoForm, modificarproyectoForm, seleccionarProyectoForm, importarRolForm
from proyectos.models import Proyecto
from proyectos.views import nuevoProyecto, getProyecto, updateProyecto, guardarCamposdeProyecto
from userStory.forms import crearHistoriaForm, seleccionarHistoriaForm, modificarHistoriaForm, eliminarHistoriaForm, cargarHorasHistoriaForm, asignarEncargadoForm,\
    asignarDesarrolladorForm,asignaryestimarHistoria
from userStory.models import Historia
from userStory.views import nuevaHistoria, updateHistoria, asignarEncargado

from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from django.contrib import auth

# Hola mundo para probar django
@login_required
def saludo(request):
    """
    Metodo que es ejecutado para mostrar un mensaje de saludo al usuario loggeado en el sistema

    :param request: consulta recibida
    :return: respuesta
    """

    return render(request, "rolCreado.html", {"nombre": "Jose"})

# Para acceder directamente a los archivos guardados en el directorio docs
# (Todavia no se ha implementado)
def documentaciones(request):
    """
    Metodo para acceder directamente a los archivos referentes a la documentacion del sistema

    :param request: consulta recibida
    :return: respuesta: de redireccionamiento
    """

    return render(request, "html/index.html", {})



def accesoDenegado(request):
    return render(request, "403.html")
##VISTAS RELACIONADAS AL MANEJO DE ROL

@login_required
@user_passes_test(lambda u: u.is_staff,login_url="/AccesoDenegado/")
def step1_CrearRol(request):
    """
    Metodo auxiliar para la creacion de roles del sistema

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


#@login_required
#@permission_required('auth.add_group', raise_exception=True)
@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
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


@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
def step1_asignarRol(request):
    """
    Metodo auxiliar para la asignacion de roles a usuarios del sistema

    :param request: solicitud recibida
    :return: respuesta a la solicitud de ASIGNAR ROL
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


#@login_required
#@permission_required('auth.add_group', raise_exception=True)
@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
def step2_asignarRol(request):
    """
    Metodo para la asignacion de roles a usuarios del sistema

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
            user_object = User.objects.get(email=user_name)
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

            #Email 1.2 de rol asignado a usuario.
            email_rolAsignado(user_object, rol_object, proyecto_object)

            #-----------------------------------


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
    """
    Metodo auxiliar que ayuda a preparar los datos necesarios para el formulario de asignacion de roles

    :param request: solicitud recibida
    :return: void
    """

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
        usuarios_names.append((u.email, u.email))

    request.session['usuario_names'] = usuarios_names
    request.session['roles_name'] = roles


# @login_required
# @permission_required('auth.delete_group', raise_exception=True)

def eliminarRol(request):
    """
    Metodo para la eliminacion de roles del sistema

    :param request: solicitud recibida
    :return: respuesta: a la solicitud de ELIMINAR ROL
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

@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
def step1_eliminarRol(request):
    """
    Metodo auxiliar para seleccionar un rol del sistema que se desea eliminar

    :param request: solicitud recibida
    :return: respuesta a la solicitud de ELIMINAR ROL
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


#@login_required
#@permission_required('auth.add_group', raise_exception=True)
@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
def step2_eliminarRol(request):
    """
    Metodo auxiliar para seleccionar un rol del sistema que se desea eliminar

    :param request: solicitud recibida
    :return: respuesta a la solicitud de ELIMINAR ROL
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


@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
def step1_modificarRol(request):
    """
    Metodo auxiliar para la seleccion del rol que se desea modificar

    :param request: solicitud recibida
    :return: respuesta a la solicitud de MODIFICAR ROL
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


#@login_required
#@permission_required('auth.add_group', raise_exception=True)
@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
def step2_modificarRol(request):
    """
    Metodo auxiliar para la seleccion del rol que se desea modificar

    :param request: solicitud recibida
    :return: respuesta a la solicitud de MODIFICAR ROL
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
#@login_required
#@permission_required('auth.change_group', raise_exception=True)
@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
def step3_modificarRol(request):
    """
    Metodo para la modificacion de roles del sistema

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
    Metodo para importar roles del sistema a un proyecto

    :param request: solicitud recibida
    :return: respuesta a la solicitud de IMPORTAR ROL
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


#@login_required
#@staff_member_required
@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
def registrarUsuario(request):
    """
    Metodo para registrar usuarios al sistema

    :param request: solicitud recibida
    :return: respuesta: a la solicitud de REGISTRAR USUARIO
    """

    if request.method == "POST":
        formulario = registroDeUsuariosForm(request.POST,request=request.session)
        if (formulario.is_valid()):
            datos = formulario.cleaned_data
            correo_usuario = formulario.cleaned_data['Usuario']
            estado = formulario.cleaned_data['Habilitado']
            # Acciones a realizar con el form
            registrar_usuario(correo_usuario, estado)

            return render(request, "outputRegistrarUsuario.html", {"usuario": datos})
    else:

        lista= User.objects.all()
        miembros = []
        for l in lista:
            miembros.append((l.email, l.email))

        request.session['miembros']=miembros
        formulario = registroDeUsuariosForm(request=request.session)

    return render(request, "RegistrarUsuario.html", {"form": formulario})


# VISTAS RELACIONADAS AL MANEJO DE PROYECTOS
#@login_required
#@permission_required('proyectos.add_proyecto', raise_exception=True)
@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
def crearProyecto(request):
    """
    Metodo para la creacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR PROYECTO
    """

    if request.method == "POST":
        formulario = crearproyectoForm(request.POST, request=request.session)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosProyecto = formulario.cleaned_data
            miembros = formulario.cleaned_data["miembros"]
            proyecto = nuevoProyecto(formulario.cleaned_data)

            # proyecto = getProyecto(formulario.cleaned_data['nombre'])
            asociarProyectoaUsuario(proyecto, miembros)

            #Email-1 Agregar usuario a proyecto. Pero sin especificar su rol
            email_nuevoProyecto(proyecto, miembros)

            #-----------------------------------
            return render(request, "outputcrearProyecto.html", {"proyectoCreado": datosProyecto})
    else:
        #Lista de miembros
        us=User.objects.all().exclude(username=['admin','Admin'])
        usuarios=[]
        for u in us:
            usuarios.append((u.email,u.email))

        request.session['miembros']=usuarios
        formulario = crearproyectoForm(request=request.session)
    return render(request, "crearProyecto.html", {"form": formulario})


@login_required
@permission_required('proyectos.change_proyecto', raise_exception=True)
def modificarProyecto(request):
    """
    Metodo para la modificacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de MODIFICAR PROYECTO
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


#@login_required
#@permission_required('proyectos.change_proyecto', raise_exception=True)
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() != 0 or u.is_superuser,login_url="/AccesoDenegado/")
def modificarProyecto2(request,id_proyecto):
    """
    Metodo para la modificacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de MODIFICAR PROYECTO
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

                print(" Listas de miembros -> ",miembros)

                print(" Listas de miembros -> ", usuarios)

                updateProyecto(formulario.cleaned_data)

                proyecto = getProyecto(idproyecto)

                # se agrega los usuarios nuevos
                asociarProyectoaUsuario(proyecto, usuarios)
                email_nuevoProyecto(proyecto, usuarios)
                # se elimina los usuarios viejos

                if(verificarOcupaciondemiembros(id_proyecto,miembros)):


                    desasociarUsuariodeProyecto(proyecto,miembros)
                    email_excluidoDelProyecto(proyecto, miembros)
                    miembrosActuales = User.objects.filter(proyecto=idproyecto)
                    # Retornar mensaje de exito
                    return render(request, "outputmodificarProyecto.html",
                              {"proyectoCreado": datosProyecto, "members": miembrosActuales})
                else:
                    return render(request, "Condicion_requerida.html", {"mensaje": "No puede quitar a los usuarios que selecciono ya que algunos de ellos necesita ser sustituido en el sprint activo"})

        else:
            #usuarioActual = User.objects.get(username=request.user.username)
            #if (usuarioActual.proyecto == None):
            #    mensaje = "Usted no forma parte de ningun proyecto"
            #    return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
            #else:
                proyecto_seleccionado=Proyecto.objects.get(id=id_proyecto)
                guardarCamposdeProyecto(request, proyecto_seleccionado)
                formulario = modificarproyectoForm(request=request.session)
                return render(request, "modificarProyecto.html", {"form": formulario})
    except AttributeError:
        print("El usuario no posee ningun proyecto")
        messages.error(request, 'El usuario no posee ningun proyecto')
        return redirect(inicio)



def verificarOcupaciondemiembros(id_proyecto,emails):
    proyecto_seleccionado = Proyecto.objects.get(id=id_proyecto)

    usuarios=[]
    for e in emails:
        usuarios.append(User.objects.get(email=e))

    for u in usuarios:
        if(len(Historia.objects.filter(proyecto=proyecto_seleccionado,estados="EN_CURSO",encargado=u))!=0):
            return False

    return True




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

#@login_required
#@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() == 0,login_url="/AccesoDenegado/")
@login_required
@user_passes_test(lambda u: u.is_superuser,login_url="/AccesoDenegado/")
def eliminarProyecto2(request,id_proyecto):
    """
    Metodo para la eliminacion de proyectos

    :param request: solicitud recibida
    :return: respuesta: a la solicitud de ELIMINAR PROYECTO
    """
    ProyectoSeleccionado=Proyecto.objects.get(id=id_proyecto)

    Historia.objects.filter(proyecto=id_proyecto).delete()

    proyecto = model_to_dict(ProyectoSeleccionado)
    sprints = proyecto["id_sprints"]
    for s in sprints:
        s.delete()

    historias = Historia.objects.filter(proyecto=id_proyecto)
    for h in historias:
        h.delete()



    lista = UserProyecto.objects.filter(proyecto=ProyectoSeleccionado)
    miembros = []
    for l in lista:
        miembros.append(l.usuario.email)



    # desasociamos proyecto con ususario
    desasociarUsuariodeProyecto(ProyectoSeleccionado,miembros)

    # Eliminamos proyecto
    ProyectoSeleccionado.delete()

    # Retornar mensaje de exito
    #return render(request, "outputEliminarProyecto.html", {"Proyectoeliminado": ProyectoSeleccionado})

    return redirect(inicio)


# La logica de Roles aun no revisado.
def swichProyecto(request, id):
    """
    Metodo para cambiar de un proyecto a otro con las reasignaciones de roles correspondiente

    :param request: Solicitud recibida
    :param id: identificador del proyecto
    :return: void
    """

    u = User.objects.get(username=request.user.username)
    p = Proyecto.objects.get(id=id)
    u.proyecto = p

    if UserProyecto.objects.filter(usuario=u, proyecto=p).exists():
        print("Esta asociado al proyecto, reasignando rol...")

        proy = UserProyecto.objects.get(usuario=u, proyecto=p)
        if(proy.rol_name!=""):
            rol_object = Group.objects.get(name=proy.rol_name)

        # Agrego al usuario al rol
        # Limpiar antiguo rol del usuario para el cambio
            print("Limpiando antiguos roles")
            u.groups.clear()
        # enlazar con el rol asignado para el proyecto
            enlazar_Usuario_con_Rol(u, rol_object)
            registrar_usuario(u.email, 'True')



    u.save()
    return redirect(inicio)


# ----------------------------------------------------
@login_required
def getPermisos(request, listaPermisos):
    """
    Metodo de gestion y asignacion de permisos a los usuarios del sistema

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
    Metodo auxiliar para la realizacion del Sprint Planning de un proyecto

    :param request: solicitud recibida
    :return: respuesta a la solicitud de SPRINT PLANNING
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
            proy = usuarioActual.proyecto
            if (len(proy.id_sprints.filter(estados="PLANNING")) == 0):
                request.session['proyecto'] = proy.id
                formulario = crearSprintForm(request=request.session)
                return render(request, "SprintPlanning_1.html", {"form": formulario})
            else:
                mensaje = "Ya existe un sprint en planning"
                return render(request, "Condicion_requerida.html", {"mensaje": mensaje})

    return render(request, "SprintPlanning_1.html", {"form": formulario})


def step2_SprintPlanning(request):
    """
    Metodo para la seleccion de desarrolladores en el Sprint Planning

    :param request: solicitud recibida
    :return: respuesta a la solicitud de SPRINT PLANNING
    """

    proyecto_actual = Proyecto.objects.get(id=request.session['proyecto'])
    sprint_actual = Sprint.objects.get(id=request.session['sprint_planning_id'])
    usuarios = []

    PosiblesIntegrantes = UserProyecto.objects.filter(proyecto=proyecto_actual, rol_name="Desarrollador")

    for elemento in PosiblesIntegrantes:
        u = UserSprint.objects.filter(proyecto=proyecto_actual, usuario=elemento.usuario, sprint=sprint_actual)
        if (len(u) == 0):
            usuarios.append(elemento.usuario)

    return render(request, "SprintPlanning_2.html", {"miembros": usuarios})


def asignarCapacidad(request, id):
    """
    Metodo para asignar la capacidad de trabajo de un desarrollador

    :param request: Solicitud recibida
    :param id: identificador de usuario
    :return: respuesta a la solicitud ASIGNAR CAPACIDAD
    """

    if request.method == 'POST':
        form = asignarcapacidadForm(request.POST)
        print(f"form : {form}")
        if (form.is_valid()):
            capacidad = form.cleaned_data['capacidad']
            print("LA CAPACIDAD ES : ", capacidad)
            if capacidad > 0:
                print("Entro en el prime if")
                usuario = User.objects.get(id=id)
                proyecto_actual = Proyecto.objects.get(id=request.session['proyecto'])
                sprint_en_planning = Sprint.objects.get(id=request.session['sprint_planning_id'])

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
    Metodo para la asignacion de users storys del product backlog al sprint backlog en el Sprint Planning

    :param request: solicitud recibida
    :return: respuesta a la solicitud de SPRINT PLANNING
    """

    proyectoActual = Proyecto.objects.get(id=request.session['proyecto'])
    sprintActual = Sprint.objects.get(id=request.session['sprint_planning_id'])

    calendarioParaguay = Paraguay()
    fechaInicio = sprintActual.fecha_inicio
    fechaFin = sprintActual.fecha_fin
    dias_de_sprint = calendarioParaguay.get_working_days_delta(fechaInicio, fechaFin) + 1

    capacidad_sprint_horas = dias_de_sprint * 24

    # Lista 1 y 2 son las historias del proyecto y del sprint actualmente
    Lista1 = Historia.objects.filter(proyecto=proyectoActual, estados="")
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

    capacidad_ocupada_por_historias = 0
    for p in prioridades:
        for h in Lista2:
            if h.prioridad == p:
                sprintbacklog.append(h)
                capacidad_ocupada_por_historias = capacidad_ocupada_por_historias + h.horasEstimadas

    tablatemporal = UserSprint.objects.filter(proyecto=proyectoActual, sprint=sprintActual)
    developers = []

    # La lista de los desarrolladores para el sprint actual
    for elemento in tablatemporal:
        developers.append((elemento.usuario.username, elemento.usuario.username))

    cantidaddehistorias = len(productbacklog)
    porcentaje = round((capacidad_ocupada_por_historias / capacidad_sprint_horas) * 100)

    print("LA cantidad de dias del sprint es : ", capacidad_sprint_horas,
          " y la cantidad ocupada por historias es  :  ", capacidad_ocupada_por_historias, "  EL PORCENTAJE ES : ",
          porcentaje)

    request.session['developers'] = developers
    # Formulario para el selector de usuarios
    formulario = asignarDesarrolladorForm(developers=request.session)

    return render(request, "SprintPlanning_3.html", {"Sprint": sprintActual, "p_backlog": productbacklog,
                                                     "s_backlog": sprintbacklog, "Total": cantidaddehistorias,
                                                     "form": formulario, "Porcentaje": porcentaje,
                                                     "Duracion": dias_de_sprint}
                  )


def step3_asignarEncargado(request, id, opcion):
    """
    Metodo para administrar la asignacion o remocion de encargado de un user story

    :param request: Solicitud recibida
    :param id: identificador del user story
    :param opcion: accion a realizar
    :return: Respuesta a la solicitud ASIGNAR ENCARGADO
    """

    # h = Historia.objects.get(id_historia=id)
    sprint_actual = Sprint.objects.get(id=request.session['sprint_planning_id'])
    #asigno encargado a la historia
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

        proyectoPropietario = User.objects.get(username=request.user.username).proyecto
        listaDevelopers = UserSprint.objects.filter(proyecto=proyectoPropietario, sprint=sprint_actual)

        # proyectoPropietario= User.objects.get(username=request.user.username).proyecto
        listasprints = proyectoPropietario.id_sprints

        if (not listasprints.filter(estados="INICIADO").exists()):  # No esta otro sprint iniciado actualmente
            # si tiene desarroladores y tiene historias agregadas
            if (len(listaDevelopers) != 0 and len(sprint_actual.historias.all()) != 0):

                # El siguente if es para cargar los datos para el burndown chart.
                # La verdad es que no se si el if es necesario ya que solo se puede iniciar 1 vez.
                if (len(sprint_actual.horasLaboralesIdeal) == 0):
                    calcularEsfuerzoIdeal(sprint_actual, listaDevelopers)
                else:
                    sprint_actual.horasLaboralesIdeal.clear()
                    calcularEsfuerzoIdeal(sprint_actual, listaDevelopers)

                sprint_actual.estados = 'INICIADO'
                sprint_actual.save()

                return redirect(tableroKanban)
            else:
                mensaje = "No puede iniciar este sprint ya que no se han agregado desarrolladores o el  sprint carece  de historias agregadas"
                return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
        else:
            mensaje = "No puede iniciar Otro sprint ya que esta uno actualmente en progreso"
            return render(request, "Condicion_requerida.html", {"mensaje": mensaje})

    # guardar
    if (opcion == 4):
        sprint_actual.estados = 'PLANNING'
        sprint_actual.save()
        # redireccionar a lista de sprints
        return redirect(visualizarSprintFilter)

    return redirect(step3_SprintPlanning)
    # return step3_SprintPlanning(request)


# Esta vista va a estar en lista de sprints
# MODIFICAR SPRINT

@login_required
@permission_required('Sprints.change_sprint', raise_exception=True)
def modificarSprint(request, id_sprint):
    """
    Metodo para la modificacion de sprint, se despliega un formulario con las informaciones actuales del sprint con la
    posibilidad de modificar algunos datos

    :param request: solicitud recibida
    :param id_sprint: identificador del sprint que se quiere modificar
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
        proyectoPropietario = usuarioActual = User.objects.get(username=request.user.username).proyecto

        # u = UserSprint.objects.filter(sprint=sprint_seleccionado)

        # proyectoPropietario = u.first().proyecto
        # No se agregaron developers por ello no se puede estirar el dato proyecto.
        request.session['proyecto'] = proyectoPropietario.id
        guardarCamposdeSprint(request, sprint_seleccionado, proyectoPropietario.id)
        formulario = modificarSprintForm(request=request.session)
        return render(request, "modificarSprint.html", {"form": formulario})


def eliminarSprint(request, id_sprint):
    """
    Metodo que permite la eliminacion de un sprint

    :param request: solicitud recibida
    :param id_sprint: identificador del sprint que se desea eliminar
    :return: respuesta a la solicitud de ELIMINAR SPRINT
    """

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
    print('Proyecto actual=',request.session["selected_id_proy"])

    proye=request.session["selected_id_proy"]

    #return redirect(visualizarSprint)

    return render(request, "outputEliminarSprintl.html", {"Sprint": sprint_seleccionado, "ProyectoID": proye})

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
    """
    Metodo que permite visualizar un sprint con todos sus detalles

    :param request: solicitud recibida
    :param id_sprint: identificador del sprint que se desea visualizar
    :return: respuesta a la solicitud de VISUALIZAR SPRINT
    """

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
    Metodo que posibilita visualizar el tablero kanban

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
        try:
            sprintActual = proyectoActual.id_sprints.get(estados="INICIADO")

            if usuarioActual.groups.filter(name="Scrum Master"):
                esMaster = True
            else:
                esMaster = False

            sprintActual2 = model_to_dict(sprintActual)
            listaHistorias = sprintActual2['historias']

            versionesDic = {}
            for hist in listaHistorias:
                if hist.history.filter(
                        Q(history_change_reason="comentario") & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                                history_date__lte=sprintActual2['fecha_fin'] + timedelta(days=1))).exists():

                    x = hist.history.filter(
                        Q(history_change_reason="comentario") & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                            history_date__lte=sprintActual2['fecha_fin'] + timedelta(days=1)))

                    listaDeComentarios = []
                    for z in list(x):
                        fech = z.history_date
                        if z.comentarios != '':
                            fechaComentario = fech.strftime("%d-%b-%Y : ") + z.comentarios
                        else:
                            fechaComentario = fech.strftime("%d-%b-%Y : ") + "Ninguno"

                        print("hist ", z.id_historia, "comentario=", fechaComentario)
                        if not fechaComentario in listaDeComentarios:
                            listaDeComentarios.append(fechaComentario)

                    versionesDic[hist.id_historia] = listaDeComentarios

            # print(versionesDic)
            cantidaddehistorias = len(listaHistorias)

            request.session['fecha_fin'] = sprintActual2['fecha_fin'].strftime("%Y/%m/%d")

            formulario = extenderSprintForm(dato=request.session)

            return render(request, "tableroKanban.html",
                          {"Sprint": sprintActual, "Historias": listaHistorias, "Total": cantidaddehistorias,
                           "versionesDic": versionesDic, "Master": esMaster, "form": formulario})

            # except IndexError:
            # return render(request, "Condicion_requerida.html", {"mensaje": "NO TIENE NINGUN SPRINT"})
        except ObjectDoesNotExist:
            return render(request, "Condicion_requerida.html", {"mensaje": "NO TIENE NINGUN SPRINT ACTIVO"})


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
def crearHistoria(request,id_proyecto):
    """
    Metodo que es ejecutado para crear un user story, se despliega un formulario con los campos necesarios para la creacion de
    un user story

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de crearHistoria
    """

    if request.method == "POST":
        formulario = crearHistoriaForm(request.POST, proyecto=request.session['idproyecto'])
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosHistoria = formulario.cleaned_data

            datosHistoria['proyecto'] = getProyecto(formulario.cleaned_data['proyecto'])


            nuevaHistoria(datosHistoria)

            # Retornar mensaje de exito
            return render(request, "outputCrearUserStory.html", {"historiaCreado": datosHistoria,"ID_proyecto":id_proyecto})
    else:
        #no sirve mas
        #usuarioActual = User.objects.get(username=request.user.username)
        #u = model_to_dict(usuarioActual)
        request.session['idproyecto'] = id_proyecto
        formulario = crearHistoriaForm(proyecto=request.session['idproyecto'])

    return render(request, "crearUserStory.html", {"form": formulario,"ID_proyecto":id_proyecto})


# Seleccionar historia 1
@login_required
@permission_required('userStory.add_historia', raise_exception=True)
def seleccionarHistoria(request):
    """
    Metodo para seleccionar un User Story

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
    Metodo para la modificacion de historias, se despliega un formulario con las informaciones actuales de la historia con la
    posibilidad de modificar algunos datos

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
    Metodo que permite la eliminacion de una historia de usuario

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
def sprintBacklog(request, id_sprint):
    """
    Metodo para visualizar los user story que estan como objetivos del sprint

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de SPRINT BACKLOG
    """

    sprintseleccionado = Sprint.objects.get(id=id_sprint)
    historias = sprintseleccionado.historias.all()

    return render(request, "SprintBacklog.html", {"historias": historias})


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

    return render(request, "SprintBacklog.html", {"historias": historias})


# Vista que hace la logica de cambio de estado en el kanban
#cambiar nombre a KanbanActual_Logica
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

    #Se agrega mueve la historia a la columna pendiente
    if (opcion == 1):
        #print("Encargado de historia = ", h.encargado, " el usuario actual = ", encargado)
        if (h.encargado == encargado):
            h.estados = 'PENDIENTE'
            messages.success(request, "Pasado a pendiente")
        else:
            messages.error(request, "No eres el encargado de la historia")
    #Se agrega mueve la historia a la columna En curso
    if (opcion == 2):
        #print("Encargado de historia = ", h.encargado, " el usuario actual = ", encargado)
        if (h.encargado == encargado):
            h.estados = 'EN_CURSO'
            messages.success(request, "Pasado a en curso")
        else:
            messages.error(request, "No eres el encargado de la historia")
    # Se agrega mueve la historia a la columna Finalizado
    if (opcion == 3):
        #print("Encargado de historia = ", h.encargado, " el usuario actual = ", encargado)
        if (h.encargado == encargado):
            h.estados = 'FINALIZADO'
            messages.success(request, "Finalizado")
        else:
            messages.error(request, "No eres el encargado de la historia")
    # Este es para cargar horas y comentario
    if(opcion == 5):
        if request.method == 'POST':
            form = cargarHorasHistoriaForm(request.POST)
            if (form.is_valid()):
                horas = form.cleaned_data['horas']
                comentario = form.cleaned_data['comentario']
                if horas > 0:
                    if request.user == h.encargado:
                        h.horas_dedicadas = h.horas_dedicadas + horas
                        h.comentarios = comentario
                        h._change_reason = "comentario"
                        messages.success(request, "Horas registradas")
                    else:
                        messages.error(request, "No eres el encargado de la historia")
                        messages.info(request, f"El encargado es {h.encargado}")
                else:
                    messages.error(request, 'Ingrese una hora valida')
            else:
                print("formulario invalido")

    h.save()
    return tableroKanban(request)

#No lo se Rick creo que ya no se usa
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

        sprint.save()

#esto se usa en line chart
def formatearlista(lista):
    listaStrings = []

    for i in lista:
        listaStrings.append(str(i))

    return listaStrings


# despliega el product backlog con filtro Pero del actual proyecto al que pertence el usuario actual
# No se usa mas. Este es
def search(request):
    """
    Metodo que despliega todos los Users Storys del proyecto (Product Backlog), con la posibilidad de buscar mediante filtraciones

    :param request: Solicitud recibida
    :return: Respuesta a la solicitud SEARCH
    """

    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)

    id_proyectoActual = User.objects.get(username=request.user.username)
    id_proyectoActual = id_proyectoActual.proyecto_id
    # if Historia.objects.filter(proyecto=id_proyectoActual)
    if Historia.objects.filter(proyecto=id_proyectoActual).exists():
        historia_list = Historia.objects.filter(proyecto=id_proyectoActual)
    else:
        historia_list = historia_list = Historia.objects.filter(proyecto=id_proyectoActual)
        # messages.info(request, "El proyecto no tiene historias")
        print("El proyecto no tiene historias")
    historia_filter = HistoriaFilter(request.GET, queryset=historia_list)
    return render(request, 'historialProduct.html', {'filter': historia_filter})


@permission_required('Sprints.change_sprint', raise_exception=True)
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

        # Primero se obtiene la lista de los sprints no verificados que hayan finalizado
        sprintsNoVerificados = []
        for sprint in listaSprint:
            if (not sprint.verificado) and sprint.estados == 'FINALIZADO':
                sprintsNoVerificados.append((sprint.id, sprint.sprintNumber))

        print(sprintsNoVerificados)
        if not sprintsNoVerificados:
            messages.error(request, "No hay ningun sprint finalizado")
        # desplegar selector
        messages.info(request, "seleccione un Sprint")
        if request.method == "POST":
            formulario = seleccionarSprintForm(request.POST, listaSprint=sprintsNoVerificados)
            if (formulario.is_valid()):
                sprintSeleccionado = formulario.cleaned_data['sprint']
        else:
            formulario = seleccionarSprintForm(listaSprint=sprintsNoVerificados)
            return render(request, "QA_sprint.html", {"form": formulario})

        try:
            print("Sprint seleccionado : ", sprintSeleccionado)
            sprintActual = Sprint.objects.get(id=sprintSeleccionado)
            sprintActual2 = model_to_dict(sprintActual)
            listaHistorias = sprintActual2['historias']
            versionesDic = {}
            for hist in listaHistorias:
                x = hist.history.filter(
                    Q(estados='FINALIZADO') & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                        history_date__lte=sprintActual2['fecha_fin'] + timedelta(days=1)))
                listaDeComentarios = []
                for z in list(x):
                    fech = z.history_date
                    fechaComentario = fech.strftime("%d-%b-%Y : ") + z.comentarios
                    if not fechaComentario in listaDeComentarios:
                        listaDeComentarios.append(fechaComentario)

                versionesDic[hist.id_historia] = listaDeComentarios
            # print(versionesDic)
            cantidaddehistorias = len(listaHistorias)
            print(listaHistorias)
            return render(request, "QA_sprint.html",
                          {"Sprint": sprintActual2, "Historias": listaHistorias, "Total": cantidaddehistorias,
                           "versionesDic": versionesDic})
        except IndexError:
            return render(request, "Condicion_requerida.html", {"mensaje": "NINGUNA HISRORIA PARA HACER QA"})
        except UnboundLocalError:
            return render(request, "Condicion_requerida.html", {"mensaje": "NO HAY SPRINTS PARA SELECCIONAR"})



# Vista que hace la logica de cambio de estado en el kanban
@login_required
def moverHistoriaQA(request,id_proyecto,id_sprint,id_historia, opcion):
    """
    Metodo para administrar el cambio de estado de historias en el tablero kanban

    :param request: solicitud recibida
    :param id: identificador de la historia a mover
    :param opcion: estado de la historia
    :return: tablero kanban actualizado
    """


    # aceptar en quality assurance la historia, entonces va a pasar a Release
    if (opcion == 6):
        h = Historia.objects.get(id_historia=id_historia)
        h.estados = 'RELEASE'
        messages.info(request, "Historia enviada a Release")
        h.save()
    # Rechazar la historia, vuelve al Product backlog pero con prioridad aumentada
    if (opcion == 7):
        h = Historia.objects.get(id_historia=id_historia)
        h.estados = ""
        h.prioridad = 'ALTA'
        messages.info(request, "Historia rechazada")
        messages.info(request, f"Nueva prioridad {h.prioridad}")
        h.save()

    #marcar como verificado.
    if opcion==8:
        sp=Sprint.objects.get(id=id_sprint)
        sp.verificado=True
        sp.save()
        url=""
        return redirect(visualizarSprintFilter)


    return tableroQA_Release2(request,id_sprint)


##Solo muestra los sprint sin mayor detalle
@login_required
@permission_required('Sprints.view_sprint', raise_exception=True)
def visualizarSprintFilter(request):
    """
    Metodo para la visualizacion de Sprints, con la posibilidad de realizar una busqueda por medio de filtraciones

    :param request: solicitud recibida
    :return: respuesta a la solicitud de VISUALIZAR SPRINT
    """

    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.proyecto == None):
        mensaje = "Usted no forma parte de ningun proyecto"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        proyectoActual = usuarioActual.proyecto
        listaSprint = proyectoActual.id_sprints.all()
        sprint_filter = SprintFilter(request.GET, queryset=listaSprint)
        return render(request, "historialSprint.html", {"Sprints": listaSprint, 'filter': sprint_filter})



#Esta vista es del el kanban con selector de sprint
#Inutil
def historicoSprint(request, id=''):
    """
    Metodo que permite visualizar el historial completo de un sprint dentro de un proyecto

    :param request: Solicitud recibida
    :param id: Indentificador del sprint
    :return: Respuesta a la solicitud de HISTORICO SPRINT
    """

    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.proyecto == None):
        mensaje = "Usted no forma parte de ningun proyecto"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        proyectoActual = model_to_dict(usuarioActual.proyecto)
        listaSprint = proyectoActual['id_sprints']

        # Primero se obtiene la lista de los sprints no verificados que hayan finalizado
        sprintsNoVerificados = []
        for sprint in listaSprint:
            if (not sprint.verificado) and sprint.estados == 'FINALIZADO':
                sprintsNoVerificados.append((sprint.id, sprint.sprintNumber))

        print(sprintsNoVerificados)
        if not sprintsNoVerificados:
            messages.error(request, "No hay ningun sprint finalizado")
        # desplegar selector
        messages.info(request, "seleccione un Sprint")
        if request.method == "POST":
            formulario = seleccionarSprintForm(request.POST, listaSprint=sprintsNoVerificados)
            if (formulario.is_valid()):
                sprintSeleccionado = formulario.cleaned_data['sprint']
        else:
            formulario = seleccionarSprintForm(listaSprint=sprintsNoVerificados)
            return render(request, "historicoSprint.html", {"form": formulario})

        try:
            print("Sprint seleccionado : ", sprintSeleccionado)
            sprintActual = Sprint.objects.get(id=sprintSeleccionado)
            sprintActual2 = model_to_dict(sprintActual)
            listaHistorias = sprintActual2['historias']
            versionesDic = {}
            for hist in listaHistorias:
                # x = hist.history.filter(Q(estados='EN_CURSO') & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                #    history_date__lte=sprintActual2['fecha_fin']))
                if hist.history.filter(
                        Q(history_change_reason="comentario") & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                            history_date__lte=sprintActual2['fecha_fin'] + timedelta(days=1))).exists():

                    x = hist.history.filter(
                        Q(history_change_reason="comentario") & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                            history_date__lte=sprintActual2['fecha_fin'] + timedelta(days=1)))

                    listaDeComentarios = []
                    for z in list(x):
                        fech = z.history_date
                        if z.comentarios != '':
                            fechaComentario = fech.strftime("%d-%b-%Y : ") + z.comentarios
                        else:
                            fechaComentario = fech.strftime("%d-%b-%Y : ") + "Ninguno"

                        # print("hist ", z.id_historia, "comentario=", fechaComentario)
                        if not fechaComentario in listaDeComentarios:
                            listaDeComentarios.append(fechaComentario)

                    versionesDic[hist.id_historia] = listaDeComentarios

            # print(versionesDic)

            cantidaddehistorias = len(listaHistorias)

            for hist in listaHistorias:
                if hist.history.filter(
                        Q(history_change_reason="fin_sprint") & Q(
                            history_date__lte=sprintActual2['fecha_fin'] + timedelta(days=1))).exists():
                    print("existe")
                    # x = hist.history.filter(
                    # Q(history_change_reason="fin_sprint") & Q(
                    #       history_date=sprintActual2['fecha_fin']+ timedelta(days=1))).first()

                    x = hist.history.filter(
                        Q(history_change_reason="fin_sprint") & Q(
                            history_date__lte=sprintActual2['fecha_fin'] + timedelta(days=1))).last()
                    print("historia =", x)
                    hist.nombre = x.nombre
                    hist.descripcion = x.descripcion
                    hist.prioridad = x.prioridad
                    hist.horasEstimadas = x.horasEstimadas
                    hist.horas_dedicadas = x.horas_dedicadas
                    hist.estados = x.estados
                    print("estado =", x.estados)
                    finalizo = x.history_date
                else:
                    print("No existe")

            return render(request, "historicoSprint.html",
                          {"Sprint": sprintActual, "Historias": listaHistorias, "Total": cantidaddehistorias,
                           "versionesDic": versionesDic, "finalizo": finalizo})
        except IndexError:
            return render(request, "Condicion_requerida.html", {"mensaje": "NINGUNA HISTORIA"})
        except UnboundLocalError:
            return render(request, "Condicion_requerida.html", {"mensaje": "NO HAY SPRINTS PARA SELECCIONAR"})


# --------------------------------------------------------------------#
# VISTAS NUEVAS PARA LA SECCION PROYECTO

# 1 Se llama esta funcion,   para ver la lista de proyectos
def HistorialProyectoFilter(request):
    """
    Metodo que permite tener un listado completo de proyectos asociados al usuario logueado

    :param request: Solicitud recibida
    :return: respuesta a la solicitud de HISTORIA PROYECTO FILTER
    """

    usuarioActual=User.objects.get(username=request.user.username)
    if(usuarioActual.is_superuser ):
        listaProyectos = Proyecto.objects.all()
    else:

        listaProyectos=usuarioActual.proyectos_asociados.all()


    Proyecto_filter = ProyectoFilter(request.GET, queryset=listaProyectos)

    return render(request, "historialProyecto.html", {'filter': Proyecto_filter})


# 2 cuando se seleciona la opcion de ver sprints.
@login_required
def HistorialSprintFilter(request, id_proyecto):
    """
    Metodo que permite la visualizacion de un listado de Sprints del proyecto

    :param request: solicitud recibida
    :return: respuesta a la solicitud de HISTORIAL SPRINT FILTER
    """
    request.session["selected_id_proy"] = id_proyecto
    proyecto_seleccionado = Proyecto.objects.get(id=id_proyecto)
    listaSprint = proyecto_seleccionado.id_sprints.all()

    fotodeususario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']
    usuario=User.objects.get(username=request.user.username)



    if (usuario.is_superuser):
        rol_name = "Administrador"
    else:
        proy = UserProyecto.objects.get(usuario=usuario, proyecto=proyecto_seleccionado)
        rol_name = proy.rol_name

    if(len(proyecto_seleccionado.id_sprints.filter(estados="INICIADO"))!=0):
        sprint_activo=proyecto_seleccionado.id_sprints.get(estados="INICIADO")
        request.session['fecha_fin'] = sprint_activo.fecha_fin.strftime("%Y/%m/%d")
        formulioExtender = extenderSprintForm(dato=request.session)
    else:
        formulioExtender= "No tiene sprint iniciados"


    sprint_filter = SprintFilter(request.GET, queryset=listaSprint)
    return render(request, "historialSprint.html", {"Sprints": listaSprint, 'filter': sprint_filter,
                                                    "ID_proyecto":id_proyecto,"ExtenderForm":formulioExtender,
                                                    "avatar":fotodeususario, "Rol_de_usuario": rol_name,"usuario":usuario,"proyecto":proyecto_seleccionado})


# 3 cuando se selecciona la opcion de ver el tablero kanban de un sprint finalizado de un proyecto anterior.
# esta es cuando se le toca la opcion de ver kanban , es la foto del kanban de un sprint finalizado
def KanbanHistorico(request, id_proyecto,id_sprint):
    """
    Metodo que permite visualizar el tablero kanban de un sprint finalizado

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :return: respuesta a la solicitud de KANBAN HISTORICO
    """
    sprintSeleccionado = Sprint.objects.get(id=id_sprint)
    sprintActual2 = model_to_dict(sprintSeleccionado)
    listaHistorias = sprintActual2['historias']
    versionesDic = {}

    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.is_superuser):
        fotodeusuario = "No tiene"
    else:
        fotodeusuario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']

    proyectoActual = Proyecto.objects.get(id=id_proyecto)
    item = UserProyecto.objects.get(proyecto=proyectoActual, usuario=usuarioActual)
    if (item.rol_name != ''):
        rol = item.rol_name
    else:
        rol = ""

    for hist in listaHistorias:
        if hist.history.filter(
                Q(history_change_reason="comentario") & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                    history_date__lte=sprintActual2['fecha_final'] + timedelta(days=1))).exists():

            x = hist.history.filter(
                Q(history_change_reason="comentario") & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                    history_date__lte=sprintActual2['fecha_final'] + timedelta(days=1)))

            listaDeComentarios = []

            for z in list(x):
                fech = z.history_date
                if z.comentarios != '':
                    fechaComentario = fech.strftime("%d-%b-%Y : ") + z.comentarios
                else:
                    fechaComentario = fech.strftime("%d-%b-%Y : ") + "Ninguno"

                if not fechaComentario in listaDeComentarios:
                    listaDeComentarios.append(fechaComentario)

            versionesDic[hist.id_historia] = listaDeComentarios

    cantidaddehistorias = len(listaHistorias)

    for hist in listaHistorias:
        if hist.history.filter(Q(history_change_reason="fin_sprint") & Q(
                history_date__lte=sprintActual2['fecha_final'] + timedelta(days=1))).exists():
            x = hist.history.filter(Q(history_change_reason="fin_sprint") & Q(
                history_date__lte=sprintActual2['fecha_final'] + timedelta(days=1))).last()
            hist.nombre = x.nombre
            hist.encargado = x.encargado
            hist.descripcion = x.descripcion
            hist.prioridad = x.prioridad
            hist.horasEstimadas = x.horasEstimadas
            hist.horas_dedicadas = x.horas_dedicadas
            hist.estados = x.estados
            finalizo = x.history_date
        else:
            print("No existe")
    return render(request, "KanbanHistorico.html",
                  {"Sprint": sprintSeleccionado, "Historias": listaHistorias, "Total": cantidaddehistorias,
                   "versionesDic": versionesDic, "finalizo": finalizo,"ID_proyecto":id_proyecto,"ID_sprint":id_sprint,"avatar":fotodeusuario,"usuario":usuarioActual, "proyecto":proyectoActual,"Rol_de_usuario":rol})


# 4 cuando se selecciona ver Product backlog
# despliega el product backlog
def HistorialProductBacklog(request, id_proyecto):
    """
    Metodo que permite visualizar el product backlog del proyecto

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :return: respuesta a la solicitud HISTORIAL PRODUCT BACKLOG
    """
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)


    fotodeususario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']
    usuario=User.objects.get(username=request.user.username)
    proyecto_seleccionado = Proyecto.objects.get(id=id_proyecto)


    if (usuario.is_superuser):
        rol_name = "Administrador"
    else:
        proy = UserProyecto.objects.get(usuario=usuario, proyecto=proyecto_seleccionado)
        rol_name = proy.rol_name



    if Historia.objects.filter(proyecto=proyecto_seleccionado).exists():
        historia_list = Historia.objects.filter(proyecto=proyecto_seleccionado).order_by('id_historia')
    else:
        historia_list = historia_list = Historia.objects.filter(proyecto=proyecto_seleccionado)
        # messages.info(request, "El proyecto no tiene historias")
        print("El proyecto no tiene historias")
    historia_filter = HistoriaFilter(request.GET, queryset=historia_list)
    return render(request, 'historialProduct.html', {'filter': historia_filter, 'ID_proyecto':id_proyecto,"avatar":fotodeususario,"usuario":usuario,"Rol_de_usuario": rol_name,"proyecto":proyecto_seleccionado})

#Todos los sprints deben ser verificados antes de finalizar proyecto.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() != 0,login_url="/AccesoDenegado/")
def finalizarProyecto(request, id_proyecto):
    """
    Metodo que permite finalizar un proyecto que esta en curso

    :param request: respuesta recibida
    :param id_proyecto: identificador del proyecto que se desea finalizar
    :return: respuesta a la solicitud de FINALIZAR PROYECTO
    """
    proyecto_seleccionado = Proyecto.objects.get(id=id_proyecto)
    sprints = proyecto_seleccionado.id_sprints.filter(estados="INICIADO")
    print("la longitud de sprints es : ", len(sprints))
    if (len(sprints) == 0):

        if (len(proyecto_seleccionado.id_sprints.filter(estados="FINALIZADO", verificado=False)) == 0):
            proyecto_seleccionado.estado = "FINALIZADO"
            proyecto_seleccionado.fecha_finalizacion = date.today()
            proyecto_seleccionado.save()

            #email 12
            email_proyectoFin(id_proyecto)
        else:
            mensaje = "No puede finalizar el proyecto ya que hay un sprint sin proceso QA"
            return render(request, "Condicion_requerida.html", {"mensaje": mensaje})
    else:
        mensaje = "No puede finalizar el proyecto ya que hay un sprint activo"
        return render(request, "Condicion_requerida.html", {"mensaje": mensaje})

    return redirect(inicio)


def finalizable_proyecto(proyecto_seleccionado):
    sprints = proyecto_seleccionado.id_sprints.filter(estados="INICIADO")





@login_required
@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() != 0,login_url="/AccesoDenegado/")
def iniciarProyecto(request, id_proyecto):
    """
    Metodo que permite iniciar un proyecto que esta en estado 'PENDIENTE'

    :param request: respuesta recibida
    :param id_proyecto: identificador del proyecto que se desea finalizar
    :return: respuesta a la solicitud de INICIAR PROYECTO
    """
    proyecto_seleccionado = Proyecto.objects.get(id=id_proyecto)

    miembros=UserProyecto.objects.filter(proyecto=proyecto_seleccionado)
    developers=False
    scrum=False

    for l in miembros:
        if(l.rol_name=="Scrum Master"):
             scrum=True
        if(l.rol_name=="Desarrollador"):
             developers=True

    if( scrum and developers):

        proyecto_seleccionado.estado = "INICIADO"
        proyecto_seleccionado.fecha = date.today()
        proyecto_seleccionado.save()
        #email 14
        email_proyectoIni(id_proyecto)
        url="/proyecto/"+str(id_proyecto)+"/"
        return redirect(url)
    else:
        return render(request, "Condicion_requerida.html", {"mensaje": "El proyecto aun necesita tener a sus miembros con un rol definido"})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() != 0,login_url="/AccesoDenegado/")
def finalizarOexpandirSprint(request,id_proyecto, id_sprint, opcion):
    """
    Metodo que permite finalizar o expandir un sprint

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :param opcion: accion que se desea realizar: 'finalizar' o 'expandir'
    :return: respuesta a la solicitud de FINALIZAR O EXPANDIR SPRINT
    """
    usuarioActual = User.objects.get(username=request.user.username)
    sprintActual = Sprint.objects.get(id=id_sprint)

    if opcion == 'finalizar':
        listaHistorias = sprintActual.historias.all()

        for hist in listaHistorias:
            hist._change_reason = 'fin_sprint'
            hist.save()

        # Ahora que ya se tiene el ultimo estado, procedemos a finalizar
        for hist in listaHistorias:
            if hist.estados == 'FINALIZADO':
                hist.estados = 'QUALITY_ASSURANCE'
            else:
                hist.estados = ""
                hist.encargado = None
                hist.prioridad = "ALTA"
            hist.save()
        messages.info(request, "Las historias finalizadas han ido a QA")
        messages.info(request, "Las historias NO finalizadas han vuelto con prioridad ALTA")
        sprintActual.fecha_final=date.today()# + timedelta(days=6)
        sprintActual.estados = 'FINALIZADO'
        sprintActual.save()
        url="/proyecto/"+str(id_proyecto)+"/Sprints/"
        #Email 11 de finalizar spritn
        email_sprintExtFin(id_proyecto,id_sprint,opcion,request.user)
        email_sprintFinalizado(id_proyecto,id_sprint)
        return redirect(url)

    if (opcion == "expandir"):
        if request.method == 'GET':
            #fecha = request.GET['fecha_fin']

            fecha2 = request.GET['datefilter']

            nuevafecha = datetime.strptime(fecha2, "%Y/%m/%d")
            sprintActual.fecha_fin = nuevafecha.date()
            sprintActual.save()
            proyecto=Proyecto.objects.get(id=id_proyecto)
            if(len(proyecto.id_sprints.filter(estados="PLANNING"))!=0):
                sprint_en_planning=proyecto.id_sprints.get(estados="PLANNING")
                #Calendario laboral
                calendarioParaguay = Paraguay()

                duracionSprint = calendarioParaguay.get_working_days_delta(sprint_en_planning.fecha_inicio, sprint_en_planning.fecha_fin)
                #nueva fecha de inicio
                sprint_en_planning.fecha_inicio=sprintActual.fecha_fin+timedelta(days=1)

                while not calendarioParaguay.is_working_day(sprint_en_planning.fecha_inicio):
                    sprint_en_planning.fecha_inicio = sprint_en_planning.fecha_inicio + timedelta(days=1)

                #nueva fecha de fin
                sprint_en_planning.fecha_fin = sprint_en_planning.fecha_inicio
                while duracionSprint > 0:
                    sprint_en_planning.fecha_fin = sprint_en_planning.fecha_fin + timedelta(days=1)
                    if calendarioParaguay.is_working_day(sprint_en_planning.fecha_fin):
                        duracionSprint = duracionSprint - 1

                #Si la fecha de entrega del proyecto es mayor a la de fin del sprint
                if sprint_en_planning.fecha_fin > proyecto.fecha_entrega:
                    extension = calendarioParaguay.get_working_days_delta(proyecto.fecha_entrega, sprint_en_planning.fecha_fin)
                    proyecto.fecha_entrega = sprint_en_planning.fecha_fin
                    messages.info(request, "La fecha estimada de entrega del Proyecto se ha extendido")
                    messages.info(request, f"Dias extendidos: {extension}")

                sprint_en_planning.save()
                proyecto.save()
                

            url = "/proyecto/" + str(id_proyecto) + "/Sprints/"

            #email 10 PAara los miembros del equipo del sprint extendido.
            email_sprintExtFin(id_proyecto, id_sprint, opcion, request.user)
            return redirect(url)

            # fecha = request.GET['fecha_fin']
            #sprintActual.fecha_fin = fecha
            #sprintActual.save()

    url="/proyecto/"+str(id_proyecto)+"/Sprints/"+str(id_sprint)+"/KanbanActivo/"
    return redirect(url)
    #return redirect(tableroKanban)

def infoProyecto(request, id_proyecto):
    """
    Metodo que permite una visualizacion de la informacion completa de un proyecto

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :return: respuesta a la solicitud de INFO PROYECTO
    """
    proyecto_seleccionado=Proyecto.objects.get(id=id_proyecto)

    total_sprints= len(proyecto_seleccionado.id_sprints.all())

    promedioSprint=DuracionSprints(proyecto_seleccionado.id_sprints.all())

    total_backlog=  len(Historia.objects.filter(proyecto=proyecto_seleccionado))
    if (total_backlog != 0):
        releases = len(Historia.objects.filter(proyecto=proyecto_seleccionado, estados="RELEASE"))
        completado = round(releases / total_backlog) * 100
    else:
        releases = 0
        completado=0



    #lista de miembros
    lista1=[]
    lista2=[]
    tabla_temporal=UserProyecto.objects.filter(proyecto=proyecto_seleccionado)
    for m in tabla_temporal:
        lista1.append(m.usuario)

        if(m.rol_name != ""):
            lista2.append(m.rol_name)
        else:
            lista2.append("No tiene rol")


    miembros=zip(lista1,lista2)

    #contamos la duracion del proyecto en dias
    calendarioParaguay = Paraguay()
    pasos = timedelta(days=1)
    duracion_proyecto=0
    transcurrido_proyecto=0
    fechaInicio=proyecto_seleccionado.fecha
    fechaFin=proyecto_seleccionado.fecha_entrega
    while fechaInicio <= fechaFin:
        if calendarioParaguay.is_working_day(fechaInicio):
            duracion_proyecto=duracion_proyecto+1
        if( date.today() <= fechaFin and calendarioParaguay.is_working_day(date.today())):
            transcurrido_proyecto=transcurrido_proyecto+1

        fechaInicio += pasos

    fechaInicio = proyecto_seleccionado.fecha.strftime("%m/%d/%Y")
    fechaFin = proyecto_seleccionado.fecha_entrega.strftime("%m/%d/%Y")
    try:
        fechaFinal=proyecto_seleccionado.fecha_finalizacion.strftime("%m/%d/%Y")
    except AttributeError:
        fechaFinal="No definido"



    return render(request, "info-Proyecto.html",
                  {"Proyecto":proyecto_seleccionado,"Miembros":miembros,"CantidadSprints":total_sprints,
                   "CantidadHistorias":total_backlog,"Progreso":completado,"Duracion":duracion_proyecto,
                   "Transcurrido":transcurrido_proyecto,"CantidadReleases":releases,"PromedioSprint":promedioSprint,
                   "FechaInicio":fechaInicio,"FechaFin":fechaFin,"FechaFinal":fechaFinal})


def DuracionSprints(sprints):
    """
    Metodo que calcula la duracion promedio de sprints del proyecto

    :param sprints: sprints del proyecto
    :return: respuesta a la solicitud DURACION SPRINTS
    """
    calendarioParaguay = Paraguay()

    total_sprints=len(sprints)
    suma=0

    for sprint in sprints:
        fechaInicio=sprint.fecha_inicio
        fechaFin=sprint.fecha_fin
        pasos = timedelta(days=1)
        while fechaInicio <= fechaFin:
            if calendarioParaguay.is_working_day(fechaInicio):
                suma = suma + 1
            fechaInicio += pasos


    if(total_sprints!=0):
        promedio=suma/total_sprints
    else:
        promedio=0

    return promedio



def infoUsuario(request, id_usuario):
    """
    Metodo que permite una visualizacion de la informacion completa de un usuario del sistema

    :param request: solicitud recibida
    :param id_usuario: identificador del usuario
    :return: respuesta a la solicitud de INFO USUARIO
    """
    promedio_capacidad=0
    Total_proyectos=0
    Eficiencia=0
    usuario_seleccionado=User.objects.get(id=id_usuario)
    fotodeususario = SocialAccount.objects.filter(user=usuario_seleccionado)[0].extra_data['picture']

    #Se cuenta la cantidad de proyectos que ya hizo
    lista=UserProyecto.objects.filter(usuario=usuario_seleccionado)
    listaProyecto=[]
    for l in lista:
        listaProyecto.append(l.proyecto)



    Total_proyectos=len(listaProyecto)

    sprints=UserSprint.objects.filter(usuario=usuario_seleccionado)
    total=0
    for sprint in  sprints:
        total=total+sprint.capacidad

    try:
        promedio_capacidad = total / len(sprints)
    except ZeroDivisionError:
        promedio_capacidad = 0

    try:
        promedio_capacidad=total/len(sprints)

        Eficiencia=len(Historia.objects.filter(encargado=usuario_seleccionado,estados = "RELEASE"))/len(Historia.objects.filter(encargado=usuario_seleccionado)) *100
    except ZeroDivisionError:
        Eficiencia=0

    return render(request, "info-Usuario.html",
                  {"Usuario": usuario_seleccionado, "ListaProyecto": listaProyecto, "CantidadProyectos": Total_proyectos,
                   "CapacidadPromedio": promedio_capacidad, "Eficiencia": Eficiencia, "avatar":fotodeususario})


#@permission_required('Sprints.change_sprint', raise_exception=True)
#@login_required
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() != 0 or u.is_superuser,login_url="/AccesoDenegado/")
def tableroQA_Release2(request,id_proyecto,id_sprint):
    """
    Metodo para visualizar el tablero Quality Assurance Release

    :param request: solicitud recibida
    :return: respuesta a la solicitud de TABLERO-QA RELEASE
    """
    try:
        sprintActual = Sprint.objects.get(id=id_sprint)
        sprintActual2 = model_to_dict(sprintActual)
        listaHistorias = sprintActual2['historias']
        versionesDic = {}
        for hist in listaHistorias:
            x = hist.history.filter(
                Q(estados='FINALIZADO') & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                    history_date__lte=sprintActual2['fecha_fin'] + timedelta(days=1)))
            listaDeComentarios = []
            for z in list(x):
                fech = z.history_date
                fechaComentario = fech.strftime("%d-%b-%Y : ") + z.comentarios
                if not fechaComentario in listaDeComentarios:
                    listaDeComentarios.append(fechaComentario)
            versionesDic[hist.id_historia] = listaDeComentarios

        cantidaddehistorias = len(listaHistorias)
        print(listaHistorias)

        usuarioActual = auth.get_user(request)

        if (usuarioActual.is_superuser):
            fotodeusuario = None
        else:
            fotodeusuario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']

        proyectoActual = Proyecto.objects.get(id=id_proyecto)

        item = UserProyecto.objects.get(proyecto=proyectoActual, usuario=usuarioActual)

        if (item.rol_name != ''):
            rol = item.rol_name
        else:
            rol = ""
        return render(request, "QA_sprint3.html",
                      {"Rol_de_usuario":rol,"usuario":usuarioActual,"proyecto":proyectoActual,"avatar":fotodeusuario,"Sprint": sprintActual, "Historias": listaHistorias, "Total": cantidaddehistorias,
                       "versionesDic": versionesDic,"ID_proyecto":id_proyecto,"ID_sprint":id_sprint})

    except IndexError:
        return render(request, "Condicion_requerida.html", {"mensaje": "NINGUNA HISRORIA PARA HACER QA"})
    except UnboundLocalError:
        return render(request, "Condicion_requerida.html", {"mensaje": "NO HAY SPRINTS PARA SELECCIONAR"})



def funcionalidadesQA(request,id_proyecto,id_sprint,id_historia, opcion):
    """
    Metodo para administrar las funcionalidades de Quality Assurance Release

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :param id_historia: identificador de la historia de usuario
    :param opcion: accion que se desea realizar con la historia seleccionada
    :return: respuesta a la solicitud de FUNCIONALIDADES QA
    """


    # aceptar en quality assurance la historia, entonces va a pasar a Release

    if (opcion == 6):
        h = Historia.objects.get(id_historia=id_historia)
        h.estados = 'RELEASE'
        h.extraData = ""
        messages.info(request, "Historia enviada a Release")
        h.save()

        #email de historias aceptada email 9.1
        email_actividadEnQA(h,id_proyecto,id_sprint,opcion,request.user)


    # Rechazar la historia, vuelve al Product backlog pero con prioridad aumentada
    if (opcion == 7):
        h = Historia.objects.get(id_historia=id_historia)
        h.estados = ""
        encargadoDeHistoria = h.encargado
        h.prioridad = 'ALTA'
        messages.info(request, f"historia {h.nombre} Rechazada")
        messages.info(request, f"Nueva prioridad {h.prioridad}")
        motivo = request.GET['motivo']
        h.extraData = motivo
        messages.info(request, f"correo enviado a {encargadoDeHistoria.email}")
        messages.info(request, motivo)
        #email 9.2
        # email 9.2
        email_actividadEnQA(h, id_proyecto, id_sprint, opcion, request.user)
        h.encargado = None
        h.save()


    #marcar como verificado.
    if opcion==8:
        #h = Historia.objects.get(id_historia=id_historia)
        sp=Sprint.objects.get(id=id_sprint)
        sp.verificado=True
        sp.save()
        url="/proyecto/"+str(id_proyecto)+"/Sprints/"
        #email 9.3
        #email_actividadEnQA(User, id_proyecto, id_sprint, opcion, request.user)
        sprintVerificado(id_proyecto,id_sprint,request.user)
        return redirect(url)

    url="/proyecto/"+str(id_proyecto)+"/Sprints/"+str(id_sprint)+"/QualityAssurance/"
    return redirect(url)
    #return tableroQA_Release2(request,id_sprint)




#La vistas 2 -----------------------------------------------------------------------
@login_required
def inicio(request):
    """
    Metodo para visualizar la pantalla de inicio del sistema

    :param request: solicitud recibida
    :return: respuesta a la solicitud de INICIO
    """
    usuarioActual = User.objects.get(username=request.user.username)
    if usuarioActual.groups.filter(name='registrado'):
        usuarioActual=User.objects.get(username=request.user.username)
        usuarioActual.proyecto=None
        if(usuarioActual.is_superuser ):
            listaProyectos = Proyecto.objects.all()
            fotodeususario = "No tiene"
        else:
            listaProyectos=usuarioActual.proyectos_asociados.all()
            fotodeususario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']
            #Esto es nuevo
            #listaUsuarioRolesProyecto=listaderoles(listaProyectos,usuarioActual,False)


        Proyecto_filter = ProyectoFilter(request.GET, queryset=listaProyectos)
        return render(request, "historialProyecto.html", {'filter': Proyecto_filter,'avatar':fotodeususario,'usuario':usuarioActual})
    else:
        return render(request, "registroRequerido.html", {"mail": request.user.email})




#url= /proyecto/id_proyecto/
@login_required
def homeProyecto(request,id_proyecto):
    """
    Metodo que permite visualizar la pantalla de inicio del proyecto con las opciones disponibles

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :return: respuesta a la solicitud de HOME PROYECTO
    """

    #Paso 1, realiza el swich de proyecto
    u = User.objects.get(username=request.user.username)
    p = Proyecto.objects.get(id=id_proyecto)

    if(u.is_superuser):
        rol_name="Administrador"
        fotodeususario="No tiene"
        return render(request, "Home_Proyecto.html",
                      {"ID_proyecto": id_proyecto, "avatar": fotodeususario, "Rol_de_usuario": rol_name,
                       "usuario": u, "proyecto": p})

    else:
        fotodeususario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']
        rol_name=swichProyecto2(request,u,p,id_proyecto)
        if(rol_name!=""):
            return render(request, "Home_Proyecto.html",
                          {"ID_proyecto": id_proyecto, "avatar": fotodeususario, "Rol_de_usuario": rol_name,
                           "usuario": u, "proyecto": p})

        else:
            return render(request, "Condicion_requerida.html",{"mensaje":"No tiene un rol aun definido, contactese con el administrador"})



#Modificar Historia 2
@login_required
@permission_required('userStory.change_historia', raise_exception=True)
def modificarHistoria2(request,id_proyecto,id_historia):
    """
    Metodo para la modificacion de historias, se despliega un formulario con las informaciones actuales de la historia con la
    posibilidad de modificar algunos datos

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_historia: identificador del user story
    :return: respuesta a la solicitud de MODIFICAR HISTORIA
    """

    if request.method == "POST":

        formulario = modificarHistoriaForm(request.POST, datosdelaHistoria=request.session['HistoriaSeleccionada'])
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosdeHistoria = formulario.cleaned_data

            datosdeHistoria['id_historia']=id_historia
            print(datosdeHistoria)

            updateHistoria(datosdeHistoria)
            # Retornar mensaje de exito
            return render(request, "outputmodificarHistoria.html", {"historiaModificada": datosdeHistoria,"ID_proyecto":id_proyecto})
    else:

        h=Historia.objects.get(id_historia=id_historia)

        request.session['HistoriaSeleccionada']=model_to_dict(h)

        formulario = modificarHistoriaForm(datosdelaHistoria=request.session['HistoriaSeleccionada'])

    return render(request, "modificarHistoria.html", {"form": formulario})




@login_required
@permission_required('userStory.delete_historia', raise_exception=True)
def eliminarHistoria2(request,id_proyecto,id_historia):
    """
    Metodo que permite la eliminacion de una historia de usuario

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_historia: identificador del user story
    :return: respuesta: a la solicitud de ELIMINAR HISTORIA
    """

    HistoriaSeleccionada = Historia.objects.get(id_historia=id_historia)
        # Acciones a realizar con el form
    HistoriaSeleccionada.delete()

    # Retornar mensaje de exito
    return render(request, "outputEliminarHistoria.html", {"HistoriaEliminado": HistoriaSeleccionada,"ID_proyecto":id_proyecto})




# VISTAS RELACIONADAS Al  SPRINT PLANNING

@login_required
@permission_required('Sprints.change_sprint', raise_exception=True)
def modificarSprint2(request, id_proyecto, id_sprint):
    """
    Metodo para la modificacion de sprint, se despliega un formulario con las informaciones actuales del sprint con la
    posibilidad de modificar algunos datos

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint que se quiere modificar
    :return: respuesta a la solicitud de MODIFICAR SPRINT
    """

    if request.method == "POST":
        formulario = modificarSprintForm(request.POST, request=request.session)
        if (formulario.is_valid()):
            datosSprint = formulario.cleaned_data
            fechavalida=validarfechaingresada(id_proyecto,datosSprint["fecha_inicio"],datosSprint["fecha_fin"],1)
            if (fechavalida):

                a= request.user.groups.filter(name='Scrum Master').count()

                updated_sprint = updateSprint(formulario.cleaned_data)
                url="/proyecto/"+str(id_proyecto)+"/Sprints/"+str(id_sprint)+"/FormarEquipo/"
                return redirect(url)
            else:
                proyecto = Proyecto.objects.get(id=id_proyecto)
                mensaje1="[ " + datosSprint["fecha_inicio"].strftime("%d/%m/%Y")+ " - " + datosSprint["fecha_fin"].strftime("%d/%m/%Y") + " ]"
                rangodisponible = calcularRango(proyecto)
                mensaje4 = "RANGO PERMITIDO :" + rangodisponible
                return render(request, "Condicion_Requerida_CrearSprint.html", {"NuevoSprint": mensaje1,"Permitido":mensaje4})
    else:
        proyectoPropietario = Proyecto.objects.get(id=id_proyecto)
        sprint_seleccionado = Sprint.objects.get(id=id_sprint)
        request.session['proyecto'] = proyectoPropietario.id
        guardarCamposdeSprint(request, sprint_seleccionado, proyectoPropietario)
        rango = calcularRango(proyectoPropietario)
        request.session['rango'] = rango
        formulario = modificarSprintForm(request=request.session)

        usuarioActual = auth.get_user(request)
        if (usuarioActual.is_superuser):
            fotodeusuario = None
        else:
            fotodeusuario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']

        item = UserProyecto.objects.get(proyecto=proyectoPropietario, usuario=usuarioActual)

        if (item.rol_name != ''):
            rol = item.rol_name
        else:
            rol = ""



        return render(request, "modificarSprint.html", {"form": formulario,"usuario":usuarioActual,"Rol_de_usuario":rol,"avatar":fotodeusuario,"Sprint":  sprint_seleccionado})


@login_required
#@permission_required('Sprints.add_sprint', raise_exception=True)
@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() != 0 or u.is_superuser,login_url="/AccesoDenegado/")
def step1_SprintPlanning2(request,id_proyecto):
    """
    Metodo auxiliar para la realizacion del Sprint Planning de un proyecto

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :return: respuesta a la solicitud de SPRINT PLANNING
    """

    if request.method == "POST":
        formulario = crearSprintForm(request.POST, request=request.session)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosSprint = formulario.cleaned_data

            sepuedecrear=validarfechaingresada(id_proyecto,datosSprint["fecha_inicio"],datosSprint["fecha_fin"],0)
            if (sepuedecrear):
                newSprint = nuevoSprint(datosSprint)
                request.session['sprint_planning_id'] = newSprint.id

                #email 14 Nuevo sprint en planning agregado
                email_sprintCreado(id_proyecto,newSprint.id)
                url = "/proyecto/" + str(id_proyecto) + "/Sprints/" + str(newSprint.id) + "/FormarEquipo/"
                return redirect(url)
            else:
                proyecto = Proyecto.objects.get(id=id_proyecto)
                mensaje1="[ " + datosSprint["fecha_inicio"].strftime("%d/%m/%Y")+ " - " + datosSprint["fecha_fin"].strftime("%d/%m/%Y") + " ]"
                rangodisponible=calcularRango(proyecto)
                mensaje4="RANGO PERMITIDO :"+rangodisponible
                return render(request, "Condicion_Requerida_CrearSprint.html", {"NuevoSprint": mensaje1,"Permitido":mensaje4})

    else:
        proy = Proyecto.objects.get(id=id_proyecto)

        if (len(proy.id_sprints.filter(estados="PLANNING")) == 0):
            if(len(proy.id_sprints.filter(estados="FINALIZADO",verificado=False))==0):
                request.session['proyecto'] = proy.id
                request.session['rango']=calcularRango(proy)
                formulario = crearSprintForm(request=request.session)
                return render(request, "SprintPlanning_1.html", {"form": formulario})
            else:
                mensaje = "No puede crear otro sprint, primero debe realizarse el proceso QA"
                return render(request, "Condicion_requerida.html", {"mensaje": mensaje})

        else:
            mensaje = "Ya existe un sprint en planning"
            return render(request, "Condicion_requerida.html", {"mensaje": mensaje})

    return render(request, "SprintPlanning_1.html", {"form": formulario,"ID_proyecto":id_proyecto})

#Proceso de step1_SprintPlanning2
def calcularRango(proyecto):
    """
    Metodo auxiliar del metodo 'step1_SprintPlanning2' que permite calcular el rango de tiempo disponible

    :param proyecto: proyecto actual
    :return: rango disponible
    """
    cantidad_iniciado = len(proyecto.id_sprints.filter(estados="INICIADO"))
    cantidad_finalizado = len(proyecto.id_sprints.filter(estados="FINALIZADO"))

    if (cantidad_iniciado == 0 and  cantidad_finalizado==0):
       return "[ "+ proyecto.fecha.strftime('%Y/%m/%d') +" - "+ proyecto.fecha_entrega.strftime('%Y/%m/%d') +" ]"

    if (cantidad_iniciado != 0 ):
       sprintActivo=proyecto.id_sprints.get(estados="INICIADO")
       return "[ "+ (sprintActivo.fecha_fin + timedelta(days=1)).strftime('%Y/%m/%d') +" - "+ proyecto.fecha_entrega.strftime('%Y/%m/%d') +" ]"

    if (cantidad_iniciado == 0 and cantidad_finalizado != 0):
        sps = proyecto.id_sprints.filter(estados="FINALIZADO")
        for s in sps:
            sprint_anterior = s
        return "[ " + (sprint_anterior.fecha_final + timedelta(days=1)).strftime('%Y/%m/%d') + " - " + (proyecto.fecha_entrega).strftime('%Y/%m/%d') + " ]"


#Proceso de step1_SprintPlanning2
def validarfechaingresada(id_proyecto,sp_fechaInicio,sp_fechaFin,situacion):
    """
    Metodo que permite la validacion de la fecha ingresada en el sprint planning

    :param id_proyecto: identificador del proyecto
    :param sp_fechaInicio: fecha de inicio ingresado
    :param sp_fechaFin: fecha de finalizacion estimado ingresado
    :param situacion: posicion que se encuentra el sprint; en planificacion o modificacion
    :return: respuesta a la solicitud de VALIDAR FECHA INGRESADA
    """
    esvalido=False
    pasos = timedelta(days=1)

    #Si se llama en sprint planning 1
    if(situacion==0):
        proyecto=Proyecto.objects.get(id=id_proyecto)
        cantidad_iniciado=len(proyecto.id_sprints.filter(estados="INICIADO"))
        #cantidad_planning = len(proyecto.id_sprints.filter(estados="PLANNING")) #ESTE SIEMPRE VA A SER 0 POR QUE NO AL CREAR UN NUEVO SPRINT NO DEBE HABER SPRINT EN PLANNING
        cantidad_finalizado = len(proyecto.id_sprints.filter(estados="FINALIZADO"))


        #CASO 1= NUEVO SPRINT CUANDO YA HAY UNO INICIADO
        if (cantidad_iniciado!=0):
            sprint=proyecto.id_sprints.get(estados="INICIADO")
            #si el nuevo sprint esta esta dentro del proyecto y despues de su sprint antecesor es valido
            if( (sp_fechaFin <= proyecto.fecha_entrega) and (sp_fechaInicio>sprint.fecha_fin)):
                esvalido = True

        #CASO 2= NUEVO SPRINT EN EL INICIO
        if (cantidad_finalizado == 0 and cantidad_iniciado == 0):
            if ((sp_fechaFin <= proyecto.fecha_entrega) and (sp_fechaInicio >= proyecto.fecha)):
                esvalido = True


        #CASO 3= NUEVO SPRINT CUANDO NO HAY INICIADO PERO SI CUANDO YA HAT SPRINT FINALIZADO PREVIAMENTE
        if (cantidad_finalizado!=0 and cantidad_iniciado== 0 ):
            sps = proyecto.id_sprints.filter(estados="FINALIZADO")
            for s in sps:
                sprint_anterior=s
            if ((sp_fechaFin <= proyecto.fecha_entrega) and (sp_fechaInicio > sprint_anterior.fecha_final)):
                esvalido = True

    #CUANDO SE LLAMA EN MODIFICAR SPRINT
    if (situacion == 1):
        proyecto = Proyecto.objects.get(id=id_proyecto)
        cantidad_iniciado = len(proyecto.id_sprints.filter(estados="INICIADO"))
        cantidad_finalizado = len(proyecto.id_sprints.filter(estados="FINALIZADO"))

        #CASO 1= SE MODIFICAR UN SPRINT CUANDO  NO HAY OTRO INICIADO y TAMPOCO HAY SPRINTS FINALIZADOS
        if (cantidad_iniciado==0 and cantidad_finalizado==0 ):
            if( (sp_fechaFin <= proyecto.fecha_entrega) and (sp_fechaInicio>=proyecto.fecha)):
                esvalido=True

        #CASO 2= SE MODIFICA UN SPRINT CUANDO NO HAY OTRO INICIADO PERO HAY  SPRINTS FINALIZADOS
        if (cantidad_iniciado == 0 and cantidad_finalizado != 0):
            sps = proyecto.id_sprints.filter(estados="FINALIZADO")
            for s in sps:
                sprint_anterior = s
            if ((sp_fechaFin <= proyecto.fecha_entrega) and (sp_fechaInicio > sprint_anterior.fecha_final)):
                esvalido = True

        if (cantidad_iniciado != 0):
            sprintActivo = proyecto.id_sprints.get(estados="INICIADO")
            if ((sp_fechaFin <= proyecto.fecha_entrega) and (sp_fechaInicio > sprintActivo.fecha_fin)):
                esvalido = True



       
    return esvalido


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() != 0 or u.is_superuser,login_url="/AccesoDenegado/")
def step2_SprintPlanning2(request, id_proyecto, id_sprint):
    """
    Metodo para la seleccion de desarrolladores en el Sprint Planning

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :return: respuesta a la solicitud de SPRINT PLANNING
    """

    proyecto_actual = Proyecto.objects.get(id=id_proyecto)
    #sprint_actual = Sprint.objects.get(id=request.session['sprint_planning_id'])
    sprint_actual = Sprint.objects.get(id=id_sprint)
    usuarios = []
    PosiblesIntegrantes = UserProyecto.objects.filter(proyecto=proyecto_actual, rol_name="Desarrollador")
    devs=[]
    lista= UserSprint.objects.filter(sprint=sprint_actual);
    #for l in lista:
    #    devs.append(l.usuario)



    for elemento in PosiblesIntegrantes:

        u = UserSprint.objects.filter(proyecto=proyecto_actual, usuario=elemento.usuario, sprint=sprint_actual)

        # si el usuario ya existe en la tabla entonces no hace falta agregar 2 veces. No entra en el if
        if (len(u) == 0):
            usuarios.append(elemento.usuario)

    #email 50
    #email_nuevoSprint(id_proyecto,id_sprint,usuarios)

    fotodeususario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']
    usuario = User.objects.get(username=request.user.username)
    if (usuario.is_superuser):
        rol_name = "Administrador"
    else:
        proy = UserProyecto.objects.get(usuario=usuario, proyecto=proyecto_actual)
        rol_name = proy.rol_name

    return render(request, "step2_SprintPlanning_2_2.html", {"miembros": usuarios,"desarrolladores":lista,"ID_proyecto":id_proyecto,"ID_sprint":id_sprint,"avatar":fotodeususario, "Rol_de_usuario": rol_name,"usuario":usuario,"proyecto":proyecto_actual})


#@login_required
#@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() == 0,login_url="/AccesoDenegado/")
#Es mas un proceso
def asignarCapacidad2(request, id_proyecto,id_sprint,id_usuario,opcion):
    """
    Metodo para asignar la capacidad de trabajo de un desarrollador

    :param request: Solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :param id_usuario: identificador de usuario
    :return: respuesta a la solicitud ASIGNAR CAPACIDAD
    """

    # if request.method == 'POST':
    #     form = asignarcapacidadForm(request.POST)
    #     if (form.is_valid()):
    #         capacidad = form.cleaned_data['capacidad']
    #         if capacidad > 0:
    #             usuario = User.objects.get(id=id_usuario)
    #             proyecto_actual = Proyecto.objects.get(id=id_proyecto)
    #             sprint_en_planning = Sprint.objects.get(id=id_sprint)
    #             try:
    #                 u = UserSprint.objects.get(usuario=usuario, proyecto=proyecto_actual, sprint=sprint_en_planning)
    #             except ObjectDoesNotExist:
    #                 nuevoElemento = UserSprint(usuario=usuario, proyecto=proyecto_actual, sprint=sprint_en_planning,
    #                                            capacidad=capacidad)
    #                 nuevoElemento.save()
    #             else:
    #
    #                 u.capacidad = capacidad
    #                 #email_nuevoSprint(id_proyecto, id_sprint, u)
    #                 u.save()
    #
    #         else:
    #             messages.error(request, 'Ingrese una capacidad valida')
    #     else:
    #         print("formulario invalido")

    usuario_seleccionado = User.objects.get(id=id_usuario)
    sprint_seleccionado = Sprint.objects.get(id=id_sprint)
    proyecto_seleccionado = Proyecto.objects.get(id=id_proyecto)

    if(opcion=="Agregar"):
        capacidad = int(request.GET['Capacidad'])
        if capacidad > 0:
             elemento=UserSprint(proyecto=proyecto_seleccionado,sprint=sprint_seleccionado,usuario=usuario_seleccionado,capacidad=capacidad)
             elemento.save()
        else:
            messages.error(request, 'Ingrese una capacidad valida')

    if(opcion=="Quitar"):
        elemento=UserSprint.objects.get(proyecto=proyecto_seleccionado, sprint=sprint_seleccionado,
                                  usuario=usuario_seleccionado)
        elemento.delete()

    if(opcion=="Cambiar"):
        capacidad = int(request.GET['Capacidad'])
        if capacidad > 0:
            elemento = UserSprint.objects.get(proyecto=proyecto_seleccionado, sprint=sprint_seleccionado,
                                      usuario=usuario_seleccionado)
            elemento.capacidad=capacidad
            elemento.save()
        else:
            messages.error(request, 'Ingrese una capacidad valida')


    url="/proyecto/"+str(id_proyecto)+"/Sprints/"+str(id_sprint)+"/FormarEquipo/"
    return redirect(url)



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() != 0 or u.is_superuser,login_url="/AccesoDenegado/")
def step3_SprintPlanning2(request, id_proyecto, id_sprint):
    """
    Metodo para la asignacion de users storys del product backlog al sprint backlog en el Sprint Planning

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint que se quiere modificar
    :return: respuesta a la solicitud de SPRINT PLANNING
    """

    proyectoActual = Proyecto.objects.get(id=id_proyecto)
    sprintActual = Sprint.objects.get(id=id_sprint)

    calendarioParaguay = Paraguay()
    fechaInicio = sprintActual.fecha_inicio
    fechaFin = sprintActual.fecha_fin
    dias_de_sprint = calendarioParaguay.get_working_days_delta(fechaInicio, fechaFin) + 1

    horaslaboralespordia=9
    capacidad_sprint_horas = dias_de_sprint * horaslaboralespordia

    # Lista 1 y 2 son las historias del proyecto y del sprint actualmente
    Lista1 = Historia.objects.filter(proyecto=proyectoActual, estados="")
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

    capacidad_ocupada_por_historias = 0
    for p in prioridades:
        for h in Lista2:
            if h.prioridad == p:
                sprintbacklog.append(h)
                capacidad_ocupada_por_historias = capacidad_ocupada_por_historias + h.horasEstimadas

    tablatemporal = UserSprint.objects.filter(proyecto=proyectoActual, sprint=sprintActual)
    developers = []

    # La lista de los desarrolladores para el sprint actual
    for elemento in tablatemporal:
        developers.append((elemento.usuario.username, elemento.usuario.username))

    cantidaddehistorias = len(productbacklog)
    porcentaje = round((capacidad_ocupada_por_historias / capacidad_sprint_horas) * 100)

    request.session['developers'] = developers

    formulario_asignar= asignaryestimarHistoria(developers=request.session)
    #formulario = asignarDesarrolladorForm(developers=request.session)  "form": formulario






    return render(request, "step3_SprintPlanning_3.html", {"Sprint": sprintActual, "p_backlog": productbacklog,
                                                     "s_backlog": sprintbacklog, "Total": cantidaddehistorias,
                                                     "formulario_asignar": formulario_asignar, "Porcentaje": porcentaje,
                                                     "Duracion": dias_de_sprint,"ID_proyecto":id_proyecto,"ID_sprint":id_sprint})



#Es un proceso de sprint planning 3
def step3_Funcionalidades(request, id_proyecto, id_sprint, id_historia, opcion):
    """
    Metodo para administrar la asignacion o remocion de encargado de un user story

    :param request: Solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :param id_historia: identificador del user story
    :param opcion: accion a realizar
    :return: Respuesta a la solicitud ASIGNAR ENCARGADO
    """

    # h = Historia.objects.get(id_historia=id)
    #sprint_actual = Sprint.objects.get(id=request.session['sprint_planning_id'])

    sprint_actual = Sprint.objects.get(id=id_sprint)
    #asigno encargado a la historia
    if (opcion == 1):
        h = Historia.objects.get(id_historia=id_historia)
        #if request.method == 'POST':
        #   formulario = asignaryestimarHistoria(request.POST, developers=request.session)
        #    if (formulario.is_valid()):
        #        usuarioSeleccionado = formulario.cleaned_data['encargado']
        #        encargado = User.objects.get(username=usuarioSeleccionado)
        #        h.encargado = encargado
        #        h.estados = 'PENDIENTE'
        #        h.horasEstimadas=formulario.cleaned_data['estimado']
        #        h.save()
        #        # Se le agrega al sprint
        #        sprint_actual.historias.add(h)
        #        sprint_actual.save()
        #    else:
        #        print("formulario invalido")
        if request.method == 'POST':
            usuarioSeleccionado = User.objects.get(username=request.POST['encargado'])
            h.horasEstimadas=request.POST['estimado']
            h.encargado = usuarioSeleccionado
            h.estados = 'PENDIENTE'
            h.save()
            sprint_actual.historias.add(h)
            sprint_actual.save()
            email_historiaAsignado(h, id_proyecto, usuarioSeleccionado)


    if (opcion == 2):
        h = Historia.objects.get(id_historia=id_historia)
        h.encargado = None
        h.estados = ""
        h.horasEstimadas=0
        h.save()
        sprint_actual.historias.remove(h)
        sprint_actual.save()



    # Iniciar
    if (opcion == 3):

        #proyectoPropietario = User.objects.get(username=request.user.username).proyecto
        proyectoPropietario = Proyecto.objects.get(id=id_proyecto)

        listaDevelopers = UserSprint.objects.filter(proyecto=proyectoPropietario, sprint=sprint_actual)

        # proyectoPropietario= User.objects.get(username=request.user.username).proyecto
        listasprints = proyectoPropietario.id_sprints

        if (not listasprints.filter(estados="INICIADO").exists()):  # No esta otro sprint iniciado actualmente
            # si tiene desarroladores y tiene historias agregadas
            if (len(listaDevelopers) != 0 and len(sprint_actual.historias.all()) != 0):

                # El siguente if es para cargar los datos para el burndown chart.
                # La verdad es que no se si el if es necesario ya que solo se puede iniciar 1 vez.
                if (len(sprint_actual.horasLaboralesIdeal) == 0):
                    calcularEsfuerzoIdeal(sprint_actual, listaDevelopers)
                else:
                    sprint_actual.horasLaboralesIdeal.clear()
                    calcularEsfuerzoIdeal(sprint_actual, listaDevelopers)

                sprint_actual.estados = 'INICIADO'
                sprint_actual.fecha_inicio = date.today()
                sprint_actual.save()

                #Email 20
                email_sprintIniciado(id_proyecto,id_sprint)
                url="/proyecto/"+str(id_proyecto)+"/Sprints/"+str(id_sprint)+"/KanbanActivo/"
                return redirect(url)
            else:
                mensaje = "No puede iniciar este sprint ya que no se han agregado desarrolladores o el  sprint carece  de historias agregadas"
                return render(request, "condicion_requerida_Sprint.html", {"mensaje": mensaje, "id_proyecto":id_proyecto})
        else:
            mensaje = "No puede iniciar Otro sprint ya que esta uno actualmente en progreso"
            return render(request, "condicion_requerida_Sprint.html", {"mensaje": mensaje, "id_proyecto":id_proyecto})


    # guardar
    if (opcion == 4):
        sprint_actual.estados = 'PLANNING'
        sprint_actual.save()
        #Email 2 enviar email a los encargados.
        #email_historiaAsignado(Historia, encargado)


        url="/proyecto/"+str(id_proyecto)+"/Sprints/"
        return redirect(url)

    #return redirect(step3_SprintPlanning)
    url = "/proyecto/" + str(id_proyecto) + "/Sprints/"+str(id_sprint)+"/AsignarHistorias/"
    return redirect(url)


#FUNCIONES RELACIONADAS A LAS CARACTERISTICAS DEL SPRITN


@login_required
def sprintBacklog2(request,id_proyecto,id_sprint):
    """
    Metodo para visualizar los user story que estan como objetivos del sprint

    :param request: consulta recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :return: respuesta a la solicitud de ejecucion de SPRINT BACKLOG
    """

    sprintseleccionado = Sprint.objects.get(id=id_sprint)
    if sprintseleccionado.estados == 'FINALIZADO':
        sprintActual2 = model_to_dict(sprintseleccionado)
        historias = sprintActual2['historias']
        historiasAlta = []
        historiasMedia = []
        historiasBaja = []
        for hist in historias:
            if hist.history.filter(Q(history_change_reason="fin_sprint") & Q(
                    history_date__lte=sprintActual2['fecha_final'] + timedelta(days=1))).exists():
                x = hist.history.filter(Q(history_change_reason="fin_sprint") & Q(
                    history_date__lte=sprintActual2['fecha_final'] + timedelta(days=1))).last()
                hist.nombre = x.nombre
                hist.encargado = x.encargado
                hist.descripcion = x.descripcion
                hist.prioridad = x.prioridad
                hist.horasEstimadas = x.horasEstimadas
                hist.horas_dedicadas = x.horas_dedicadas
                hist.estados = x.estados
                if(hist.prioridad == 'ALTA'):
                    historiasAlta.append(hist)
                elif(hist.prioridad == 'MEDIA'):
                    historiasMedia.append(hist)
                elif (hist.prioridad == 'BAJA'):
                    historiasBaja.append(hist)
                finalizo = x.history_date
            else:
                print("No existe")
    else:
        #El caso de que el sprint no este finalizado, es el actual
        historias = sprintseleccionado.historias.all()
        historiasAlta = sprintseleccionado.historias.filter(prioridad='ALTA')
        historiasMedia = sprintseleccionado.historias.filter(prioridad='MEDIA')
        historiasBaja = sprintseleccionado.historias.filter(prioridad='BAJA')


    usuarioActual = auth.get_user(request)

    if (usuarioActual.is_superuser):
        fotodeusuario = None
    else:
        fotodeusuario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']

    proyectoActual = Proyecto.objects.get(id=id_proyecto)

    item = UserProyecto.objects.get(proyecto=proyectoActual, usuario=usuarioActual)


    if (item.rol_name != ''):
        rol = item.rol_name
    else:
        rol = ""

    cantidaddehistorias = len(historias)
    return render(request, "SprintBacklog.html", {"cantidad_de_historias":cantidaddehistorias,"sprint":sprintseleccionado,"Rol_de_usuario":rol,"ID_proyecto":id_proyecto,"proyecto":proyectoActual,"avatar":fotodeusuario,"usuario":usuarioActual,"historiasAlta": historiasAlta,"historiasMedia": historiasMedia,"historiasBaja": historiasBaja })



#-------TABLERO KANBAN DEL SPRINT-----------#
@login_required
#ESte no se que permiso ponerle ya que diferentes roles pueden verlo.
def tableroKanban2(request,id_proyecto,id_sprint):
    """
    Metodo que posibilita visualizar el tablero kanban

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :return: respuesta a la solicitud de TABLERO KANBAN
    """

    usuarioActual = User.objects.get(username=request.user.username)
    if (usuarioActual.is_superuser):
        fotodeususario = "No tiene"
    else:
        fotodeususario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']

    proyectoActual = Proyecto.objects.get(id=id_proyecto)

    try:

        #sprintActual = proyectoActual.id_sprints.get(estados="INICIADO")
        sprintActual = Sprint.objects.get(id=id_sprint)
        if usuarioActual.groups.filter(name="Scrum Master"):
            esMaster = True
        else:
            esMaster = False

        sprintActual2 = model_to_dict(sprintActual)
        listaHistorias = sprintActual2['historias']

        #Preparacion de comentarios
        versionesDic = {}
        total_horas_estimadas=0
        for hist in listaHistorias:
            total_horas_estimadas=total_horas_estimadas+hist.horasEstimadas
            if hist.history.filter(
                    Q(history_change_reason="comentario") & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                            history_date__lte=sprintActual2['fecha_fin'] + timedelta(days=1))).exists():

                x = hist.history.filter(
                    Q(history_change_reason="comentario") & Q(history_date__gte=sprintActual2['fecha_inicio']) & Q(
                        history_date__lte=sprintActual2['fecha_fin'] + timedelta(days=1)))

                listaDeComentarios = []
                for z in list(x):
                    fech = z.history_date
                    if z.comentarios != '':
                        fechaComentario = fech.strftime("%d-%b-%Y : ") + z.comentarios
                    else:
                        fechaComentario = fech.strftime("%d-%b-%Y : ") + "Ninguno"

                    print("hist ", z.id_historia, "comentario=", fechaComentario)
                    if not fechaComentario in listaDeComentarios:
                        listaDeComentarios.append(fechaComentario)

                versionesDic[hist.id_historia] = listaDeComentarios


        cantidaddehistorias = len(listaHistorias)

        request.session['fecha_fin'] = sprintActual2['fecha_fin'].strftime("%Y/%m/%d")

        formulioExtender = extenderSprintForm(dato=request.session)

        item=UserProyecto.objects.get(proyecto=proyectoActual,usuario=usuarioActual)
        if(item.rol_name!=''):
            rol=item.rol_name
        else:
            rol=""
        calendarioParaguay = Paraguay()

        diasLaborales_py = []
        diasLaborales_py.append("Inicio")
        # 6 Se genera la lista para el eje x del line chart
        fechaInicio=sprintActual.fecha_inicio
        fechaFin=sprintActual.fecha_fin
        pasos = timedelta(days=1)

        while fechaInicio <= fechaFin:
            if calendarioParaguay.is_working_day(fechaInicio):
                diasLaborales_py.append(fechaInicio.strftime("%d-%b"))
            fechaInicio += pasos


        if calendarioParaguay.is_working_day(date.today()):
            calcularEsfuerzoReal(listaHistorias, sprintActual, diasLaborales_py, total_horas_estimadas)

            return render(request, "tableroKanban2.html",
                          {"Sprint": sprintActual, "Historias": listaHistorias, "Total": cantidaddehistorias,
                           "versionesDic": versionesDic, "Master": esMaster, "ExtenderForm": formulioExtender,"ID_proyecto":id_proyecto,"ID_sprint":id_sprint,"avatar":fotodeususario,"usuario":usuarioActual,"proyecto":proyectoActual,"Rol_de_usuario":rol})
        else:
            return render(request, "Condicion_requerida.html", {"mensaje": "No puede acceder al tablero kanban. No es un dia laboral"})


    except ObjectDoesNotExist:
        return render(request, "Condicion_requerida.html", {"mensaje": "NO TIENE NINGUN SPRINT ACTIVO"})

@login_required
def moverHistoria2(request, id_proyecto, id_sprint, id_historia, opcion):
    """request = {WSGIRequest} <WSGIRequest: GET '/proyecto/48/Sprints/92/KanbanActivo/Historia132/Op5'>
    Metodo para administrar el cambio de estado de historias en el tablero kanban

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :param id_historia: identificador de la historia a mover
    :param opcion: estado de la historia
    :return: tablero kanban actualizado
    """

    h = Historia.objects.get(id_historia=id_historia)
    encargado = User.objects.get(username=request.user.username)
    # Agregar Tiempo

    #Se mueve la historia a la columna pendiente
    if (opcion == 1):
        #print("Encargado de historia = ", h.encargado, " el usuario actual = ", encargado)
        if (h.encargado == encargado):
            h.estados = 'PENDIENTE'
            messages.success(request, "Pasado a pendiente")
            #email
            email_actividadEnKanban(h,id_proyecto,id_sprint,h.encargado,0,"",opcion)
        else:
            messages.error(request, "No eres el encargado de la historia")
    #Se mueve la historia a la columna En curso
    if (opcion == 2):
        #print("Encargado de historia = ", h.encargado, " el usuario actual = ", encargado)
        if (h.encargado == encargado):
            h.estados = 'EN_CURSO'
            messages.success(request, "Pasado a en curso")
            #email 4
            email_actividadEnKanban(h,id_proyecto,id_sprint,h.encargado,0,"",opcion)
        else:
            messages.error(request, "No eres el encargado de la historia")
    # Se mueve la historia a la columna Finalizado
    if (opcion == 3):
        #print("Encargado de historia = ", h.encargado, " el usuario actual = ", encargado)
        if (h.encargado == encargado):
            h.estados = 'FINALIZADO'
            messages.success(request, "Finalizado")
            #email 7
            email_actividadEnKanban(h,id_proyecto,id_sprint,h.encargado,0,"",opcion)
            #email 15 enfocado para los scrum masters
        else:
            messages.error(request, "No eres el encargado de la historia")
    # Este es para cargar horas y comentario
    if(opcion == 5):
        horas= int(request.GET['Horas'])

        comentario=request.GET['Comentario']
        if horas > 0:
            if request.user == h.encargado:
                h.horas_dedicadas = h.horas_dedicadas + horas
                h.comentarios = comentario
                h._change_reason = "comentario"
                messages.success(request, "Horas registradas")
                #email 3
                #email 6
                email_actividadEnKanban(h, id_proyecto, id_sprint, h.encargado, horas, comentario, opcion)

            else:
                messages.error(request, "No eres el encargado de la historia")
                messages.info(request, f"El encargado es {h.encargado}")
        else:
                messages.error(request, 'Ingrese una hora valida')


        # if request.method == 'POST':
        #    form = cargarHorasHistoriaForm(request.POST)
        #    if (form.is_valid()):
        #        horas = form.cleaned_data['horas']
        #        comentario = form.cleaned_data['comentario']
        #        if horas > 0:
        #            if request.user == h.encargado:
        #                h.horas_dedicadas = h.horas_dedicadas + horas
        #                h.comentarios = comentario
        #                h._change_reason = "comentario"
        #                messages.success(request, "Horas registradas")
        #            else:
        #                messages.error(request, "No eres el encargado de la historia")
        #                messages.info(request, f"El encargado es {h.encargado}")
        #        else:
        #            messages.error(request, 'Ingrese una hora valida')
        #    else:
        #        print("formulario invalido")

    h.save()
    url="/proyecto/"+str(id_proyecto)+"/Sprints/"+str(id_sprint)+"/KanbanActivo/"
    return redirect(url)



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() != 0 or u.is_superuser,login_url="/AccesoDenegado/")
#@login_required
#@permission_required('Sprints.delete_sprint', raise_exception=True)
def eliminarSprint2(request, id_proyecto,id_sprint):
    """
    Metodo que permite la eliminacion de un sprint

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint que se desea eliminar
    :return: respuesta a la solicitud de ELIMINAR SPRINT
    """

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

    proye=request.session["selected_id_proy"]

    #return redirect(visualizarSprint)

    #return render(request, "outputEliminarSprintl.html", {"Sprint": sprint_seleccionado, "ProyectoID": id_proyecto})
    url="/proyecto/"+str(id_proyecto)+"/Sprints/"
    return redirect(url)



#muestra el formulario para cambiar de miembro en un sprint
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Scrum Master').count() != 0 or u.is_superuser,login_url="/AccesoDenegado/")
def intercambiarMiembro(request,id_proyecto,id_sprint):
    """
    Metodo que permite el intercambio de desarrolladores de un sprint con otro del mismo proyecto

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :return: respuesta a la solicitud de INTERCAMBIAR MIEMBRO
    """
    if request.method == "POST":
        formulario= intercambiardeveloperForm(request.POST,dato=request.session)
        if (formulario.is_valid()):
            emailA = formulario.cleaned_data['miembroA']
            emailB = formulario.cleaned_data['miembroB']

            usuario1=User.objects.get(email=emailA)
            usuario2 = User.objects.get(email=emailB)
            sprint_actual = Sprint.objects.get(id=id_sprint)
            proyecto_actual=Proyecto.objects.get(id=id_proyecto)

            # lo reemplazamos en el equipo sin cambiar su capacidad.
            miembro_saliente = UserSprint.objects.get(proyecto=proyecto_actual,sprint=sprint_actual, usuario=usuario1)
            miembro_entrando = UserSprint(proyecto=proyecto_actual, sprint=sprint_actual, usuario=usuario2,capacidad=miembro_saliente.capacidad)
            miembro_saliente.delete()

            historiaspendientes = sprint_actual.historias.filter(encargado=usuario1, estados='PENDIENTE')
            historiasencurso = sprint_actual.historias.filter(encargado=usuario1, estados='EN_CURSO')


            for h in historiaspendientes:
                h.encargado = usuario2
                h.save()

            for h in historiasencurso:
                h.encargado = usuario2
                h.save()

            sprint_actual.save()
            url = "/proyecto/" + str(id_proyecto) + "/Sprints/"
            return redirect(url)
    else:
        proyecto_actual = Proyecto.objects.get(id=id_proyecto)
        sprint_actual = Sprint.objects.get(id=id_sprint)


        lista = UserSprint.objects.filter(proyecto=proyecto_actual, sprint=sprint_actual)

        lista2 = UserProyecto.objects.filter(proyecto=proyecto_actual)
        disponibles = []

        equipo = []
        for l in lista:
            equipo.append((l.usuario.email,l.usuario.email))




        for i in lista2:
            for j in lista:
                if (i.usuario.email != j.usuario.email and i.rol_name=="Desarrollador"):
                    disponibles.append((i.usuario.email,i.usuario.email))

        if(len(equipo)==0):
            # el sprint aun no tiene miembros
            return render(request, "Condicion_requerida.html", {"mensaje": "El sprint aun no tiene desarrolladores"})

        request.session['equipo'] = equipo
        request.session['disponibles'] = disponibles
        formulario = intercambiardeveloperForm(dato=request.session)
    return render(request, "IntercambiarMiembro.html", {"form": formulario})


#Es un proceso
def swichProyecto2(request,u,p, id_proyecto):
    """
    Metodo para cambiar usuario de un proyecto a otro con las reasignaciones de roles correspondiente

    :param request: Solicitud recibida
    :param u: usuario
    :param p: proyecto
    :return: void
    """


    u.proyecto = p
    if UserProyecto.objects.filter(usuario=u, proyecto=p).exists():
        proy = UserProyecto.objects.get(usuario=u, proyecto=p)
        #Si el usuario tiene rol en el proyecto entonces se realiza el cambio de roles
        if(proy.rol_name!=""):
            rol_object = Group.objects.get(name=proy.rol_name)
            print("Limpiando antiguos roles")
            u.groups.clear()
        # enlazar con el rol asignado para el proyecto
            enlazar_Usuario_con_Rol(u, rol_object)
            registrar_usuario(u.email, 'True')
            u.save()
            return proy.rol_name
        else:
            return proy.rol_name
            print("No tiene ROl")


def infoSprint(request,id_proyecto,id_sprint):
    """
    Metodo que permite una visualizacion de la informacion completa de un proyecto

    :param request: solicitud recibida
    :param id_proyecto: identificador del proyecto
    :return: respuesta a la solicitud de INFO PROYECTO
    """
    proyecto_seleccionado=Proyecto.objects.get(id=id_proyecto)
    sprint_seleccionado=Sprint.objects.get(id=id_sprint)

    #total_sprints= len(proyecto_seleccionado.id_sprints.all())
    total_historias=len(sprint_seleccionado.historias.all())
    #promedioSprint=DuracionSprints(proyecto_seleccionado.id_sprints.all())

    #total_backlog=  len(Historia.objects.filter(proyecto=proyecto_seleccionado))

    if(sprint_seleccionado.verificado):
        verificado=True
    else:
        verificado=False



    #lista de miembros
    lista1=[]
    #lista2=[]
    tabla_temporal=UserSprint.objects.filter(proyecto=proyecto_seleccionado,sprint=sprint_seleccionado)
    for m in tabla_temporal:
        lista1.append(m.usuario)

        #if(m.rol_name != ""):
        #    lista2.append(m.rol_name)
        #else:
        #    lista2.append("No tiene rol")


    #miembros=zip(lista1,lista2)

    miembros = lista1

    #contamos la duracion del proyecto en dias
    calendarioParaguay = Paraguay()
    pasos = timedelta(days=1)
    #duracion_proyecto=0
    duracion_sprint=0
    #transcurrido_proyecto=0
    transcurrido_sprint=0
    #fechaInicio=proyecto_seleccionado.fecha
    #fechaFin=proyecto_seleccionado.fecha_entrega
    fechaInicio=sprint_seleccionado.fecha_inicio
    fechaFin=sprint_seleccionado.fecha_fin
    while fechaInicio <= fechaFin:
        if calendarioParaguay.is_working_day(fechaInicio):
            #duracion_proyecto=duracion_proyecto+1
            duracion_sprint=duracion_sprint+1
        if( date.today() <= fechaFin and calendarioParaguay.is_working_day(date.today())):
            #transcurrido_proyecto=transcurrido_proyecto+1
            transcurrido_sprint = transcurrido_sprint+1

        fechaInicio += pasos

    #fechaInicio = proyecto_seleccionado.fecha.strftime("%m/%d/%Y")
    fechaInicio = sprint_seleccionado.fecha_inicio.strftime("%m/%d/%Y")

    #fechaFin = proyecto_seleccionado.fecha_entrega.strftime("%m/%d/%Y")
    fechaFin = sprint_seleccionado.fecha_fin.strftime("%m/%d/%Y")

    try:
        fechaFinal = sprint_seleccionado.fecha_final.strftime("%m/%d/%Y")
    except AttributeError:
        fechaFinal="Sin proceso QA"



    return render(request, "info-Sprint.html",
                  {"Proyecto":proyecto_seleccionado,"Sprint":sprint_seleccionado,"Miembros":miembros,"CantidadHistorias":total_historias,
                   "Duracion":duracion_sprint,
                   "Transcurrido":transcurrido_sprint,
                   "FechaInicio":fechaInicio,"FechaFin":fechaFin,"FechaFinal":fechaFinal})






def BurndownChart(request,id_proyecto,id_sprint):
    """
    Metodo para Graficar el burndown chart en un gráfico de linea

    :param request: solicitud recibida
    :return: grafico de burndown chart
    """

    calendarioParaguay = Paraguay()
    proyecto = Proyecto.objects.get(id=id_proyecto)
    sprintActual = Sprint.objects.get(id=id_sprint)




    # 2- calculamos la capacidad del equipo
    capacidad_de_equipo = 0  #suma de las capacidades de los miembros del sprint
    desarrolladores = UserSprint.objects.filter(sprint=sprintActual)
    for desarrollador in desarrolladores:
        capacidad_de_equipo = capacidad_de_equipo + desarrollador.capacidad

    # 3- se extrae la lista de historias.
    #sprintActual2 = model_to_dict(sprintActual)
    #listaHistorias = sprintActual2['historias']
    listaHistorias = sprintActual.historias.all()
    cantidad_total_historia = len(listaHistorias)

    # Los miembros en forma de cadena para saber su estado
    total_horas_estimadas = 0
    miembrosSprint = []
    for hist in listaHistorias:
        total_horas_estimadas = total_horas_estimadas + hist.horasEstimadas
        try:
            #no entiendo
            lastlog = hist.encargado.last_login.strftime("%d/%b - %I:%M %p")
            miembro = f"{hist.encargado.email}\nUlt. activo : {lastlog}"
            if not miembro in miembrosSprint:
                miembrosSprint.append(miembro)
        except AttributeError:
            print(f"la historia {hist} aun no tiene encargado")
        # esto no se toca

    # 4 Se calcula la cantidad de dias del sprint
    #fechaInicio = sprintActual2['fecha_inicio']
    #fechaFin = sprintActual2['fecha_fin']
    fechaInicio = sprintActual.fecha_inicio
    fechaFin = sprintActual.fecha_fin


    dias_de_sprint = calendarioParaguay.get_working_days_delta(fechaInicio, fechaFin) + 1
    # 5 Se inicializan las variables que son necesarios para el line chart
    diasLaborales_py = []
    horasLaborales_Ideal = []
    horasLaborales_Real = []
    pasos = timedelta(days=1)

    diasLaborales_py.append("Inicio")
    # 6 Se genera la lista para el eje x del line chart
    while fechaInicio <= fechaFin:
        if calendarioParaguay.is_working_day(fechaInicio):
            diasLaborales_py.append(fechaInicio.strftime("%d-%b"))
        fechaInicio += pasos

    total_horas_dedicadas = 0

    # 8 Calculamos el efuerzo real.
    # Calcula la lista de esfuerzo real y lo guarda en el modelo
    #esto ha sido comentado
    #if(sprintActual.estados=="INICIADO"):
    #    calcularEsfuerzoReal(listaHistorias, sprintActual, diasLaborales_py, total_horas_estimadas)


    #horasLaborales_Ideal.append("Dia 0")
    #horasLaborales_Real.append("Dia 0")
    # SE PREPARAN LAS 2 LINEAS

    for i in sprintActual.horasLaboralesIdeal:
        horasLaborales_Ideal.append(str(i))

    # Se le da el formato actual para el line chart

    for i in sprintActual.horasLaboralesReal:
        horasLaborales_Real.append(str(i))

    usuarioActual = auth.get_user(request)
    if (usuarioActual.is_superuser):
        fotodeusuario = None
    else:
        fotodeusuario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']

    item = UserProyecto.objects.get(proyecto=proyecto, usuario=usuarioActual)


    if (item.rol_name != ''):
        rol = item.rol_name
    else:
        rol = ""

    return render(request, "lineChart.html",
                      {"usuario":usuarioActual,"Rol_de_usuario":rol,"avatar":fotodeusuario,"Sprint": sprintActual,
                       "Historias": listaHistorias,
                       "Total": cantidad_total_historia,
                       "diasLaborales": ','.join(diasLaborales_py),
                       "horasLaboralesIdeal": ','.join(horasLaborales_Ideal),
                       "horasLaboralesReal": ','.join(horasLaborales_Real),
                       "cantidadDias": dias_de_sprint,
                       "miembros": miembrosSprint,
                       "proyecto" : proyecto})



def calcularEsfuerzoReal(Historias, sprint_seleccionado, dias_laborales, total_horas_estimadas):
    """
    Metodo para obtener el esfuerzo diario en las historias de usuario, necesario para graficar el burndown chart

    :param Historias: Lista de Historias
    :param sprint: Sprint actual
    :param Dias: Dia actual
    :return: void
    """
    # FASE 1
    # Calcula el esfuerzo total del dia
    total_horas_dedicadas = 0
    for historia in Historias:
        total_horas_dedicadas = total_horas_dedicadas + historia.horas_dedicadas



    esfuerzo_del_dia = total_horas_estimadas - total_horas_dedicadas

    # FASE 2
    # Se agrega a el esfuerzo a la lista
    calendarioParaguay = Paraguay()
    hoy = datetime.today()

    #hoy = hoy + timedelta(days=1) #Este parametro se toca para poder avanzar en el dia
    #print("Es dia laboral",hoy)
    #if calendarioParaguay.is_working_day(hoy):
    print("Es dia laboral")
    hoy = hoy.strftime("%d-%b")

    print("la lista de dias laborales es ",dias_laborales)
    print("FEcha evaluada = ", hoy)

    #la fecha de hoy esta dentro de los dias laborales del sprint
    #si posicion=0 entonces es el dia 1,
    #si posicion=1 entonces es el dia 2
    if (hoy in dias_laborales):
        posicion = dias_laborales.index(hoy)
    # si todavia no hay elementos en la lista de horas laborales reales se agrega
        if (len(sprint_seleccionado.horasLaboralesReal) == 0):
            sprint_seleccionado.horasLaboralesReal.insert(posicion, esfuerzo_del_dia)
        else:  # se inserta en dicha posicion y se quita el elemento que antes estaba ahi.
            try:
                sprint_seleccionado.horasLaboralesReal.insert(posicion, esfuerzo_del_dia)
                sprint_seleccionado.horasLaboralesReal.pop(posicion + 1)
            except IndexError:
                print("posicion+1 no existia")

        sprint_seleccionado.save()


def calcularEsfuerzoIdeal(sprint_seleccionado, desarrolladores):
    """
    Metodo que permite el calculo del esfuerzo ideal para el sprint

    :param sprint_seleccionado: sprint seleccionado
    :param desarrolladores: desarrolladores del sprint seleccionado
    :return: respuesta a la solicitud de CALCULAR ESFUERZO IDEAL
    """
    calendarioParaguay = Paraguay()

    # 2- calculamos la capacidad del equipo
    capacidad_de_equipo = 0
    for desarrollador in desarrolladores:
        capacidad_de_equipo = capacidad_de_equipo + desarrollador.capacidad

    # 3- se extrae la lista de historias.
    listaHistorias = sprint_seleccionado.historias.all()


    # 4 Se calcula la cantidad de dias del sprint
    fechaInicio = sprint_seleccionado.fecha_inicio
    fechaFin = sprint_seleccionado.fecha_fin

    diasLaborales_py = []
    pasos = timedelta(days=1)

    # 6 Se genera la lista para el eje x del line chart

    diasLaborales_py.append("Inicio")
    while fechaInicio <= fechaFin:
        if calendarioParaguay.is_working_day(fechaInicio):
            diasLaborales_py.append(fechaInicio.strftime("%d-%b"))
        fechaInicio += pasos

    total_horas_estimadas = 0
    for h in listaHistorias:
        total_horas_estimadas = total_horas_estimadas + (h.horasEstimadas)


    #Opcion 2 planteado por edher
    dias_de_sprint=len(diasLaborales_py)-1
    dias_de_sprint2 = calendarioParaguay.get_working_days_delta(fechaInicio, fechaFin) + 1
    print("cantidad de dias con el len = "+str(dias_de_sprint))

    print("cantidad de dias con el get working days = " + str(dias_de_sprint2))
    promedio_de_quemado=total_horas_estimadas/dias_de_sprint

    #esto es para que ambos tengan en el inicio el mismo numero de horas
    sprint_seleccionado.horasLaboralesIdeal.append(total_horas_estimadas)
    sprint_seleccionado.horasLaboralesReal.append(total_horas_estimadas)

    for dia in diasLaborales_py:
        total_horas_estimadas = total_horas_estimadas - promedio_de_quemado
        if(total_horas_estimadas >0 ):
            sprint_seleccionado.horasLaboralesIdeal.append(total_horas_estimadas)
        else:
            sprint_seleccionado.horasLaboralesIdeal.append(0)
            break





    #bandera=dias_de_sprint
    #while(bandera>0):
    #    total_horas_estimadas = total_horas_estimadas - promedio_de_quemado
    #    if (total_horas_estimadas > 0):
    #        sprint_seleccionado.horasLaboralesIdeal.append(total_horas_estimadas)
    #
    #    else:
    #        sprint_seleccionado.horasLaboralesIdeal.append(0)
    #    bandera=bandera-1


def informe_Sprint(request,id_proyecto,id_sprint):
    """
    Metodo para generar el reporte del Sprint actual o finalizado

    :param request: Solicitud recibida
    :param id_proyecto: identificador del proyecto
    :param id_sprint: identificador del sprint
    :return: Impresion de la historia con sus respectivos campos (nombre, encargado, descripcion, prioridad, horas Estimadas y dedicadas y su estado)
    """

    sprintseleccionado = Sprint.objects.get(id=id_sprint)
    #Caso que el sprint ya haya finalizado, usar el historico de la historia en el punto de fin
    if sprintseleccionado.estados == 'FINALIZADO':
        print("Sprint finalizado")
        sprintActual2 = model_to_dict(sprintseleccionado)
        historias = sprintActual2['historias']
        historiasAlta = []
        historiasMedia = []
        historiasBaja = []
        for hist in historias:
            if hist.history.filter(Q(history_change_reason="fin_sprint") & Q(
                    history_date__lte=sprintActual2['fecha_final'] + timedelta(days=1))).exists():
                x = hist.history.filter(Q(history_change_reason="fin_sprint") & Q(
                    history_date__lte=sprintActual2['fecha_final'] + timedelta(days=1))).last()
                hist.nombre = x.nombre
                hist.encargado = x.encargado
                hist.descripcion = x.descripcion
                hist.prioridad = x.prioridad
                hist.horasEstimadas = x.horasEstimadas
                hist.horas_dedicadas = x.horas_dedicadas
                hist.estados = x.estados
                if(hist.prioridad == 'ALTA'):
                    historiasAlta.append(hist)
                elif(hist.prioridad == 'MEDIA'):
                    historiasMedia.append(hist)
                elif (hist.prioridad == 'BAJA'):
                    historiasBaja.append(hist)
                finalizo = x.history_date
            else:
                print("No existe")
    else:
        #El caso de que el sprint no este finalizado, es el actual
        historias = sprintseleccionado.historias.all()
        historiasAlta = sprintseleccionado.historias.filter(prioridad='ALTA')
        historiasMedia = sprintseleccionado.historias.filter(prioridad='MEDIA')
        historiasBaja = sprintseleccionado.historias.filter(prioridad='BAJA')


    usuarioActual = auth.get_user(request)

    if (usuarioActual.is_superuser):
        fotodeusuario = None
    else:
        fotodeusuario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']

    proyectoActual = Proyecto.objects.get(id=id_proyecto)

    item = UserProyecto.objects.get(proyecto=proyectoActual, usuario=usuarioActual)


    if (item.rol_name != ''):
        rol = item.rol_name
    else:
        rol = ""

    cantidaddehistorias = len(historias)


    context = {"cantidad_de_historias":cantidaddehistorias,"sprint":sprintseleccionado,"Rol_de_usuario":rol,"ID_proyecto":id_proyecto,"proyecto":proyectoActual,"avatar":fotodeusuario,"usuario":usuarioActual,"historiasAlta": historiasAlta,"historiasMedia": historiasMedia,"historiasBaja": historiasBaja }

    html = render_to_string("informe_US_Sprint_pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; informe_US_Sprint.pdf"

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)

    return response


def informe_Historia_Sprint(request,id_proyecto):
    """
    Metodo para generar el reporte de todos los Sprints de un proyecto(actual o finalizado)

    :param request: Solicitud recibida
    :param id_proyecto: identificador del proyecto
    :return: Impresion de la historia con sus respectivos campos (nombre, encargado, descripcion, prioridad, horas Estimadas y dedicadas y su estado)
    """

    historiasSprint = {}
    proyecto = Proyecto.objects.get(id=id_proyecto)
    for sprintseleccionado in proyecto.id_sprints.all():
        #Caso que el sprint ya haya finalizado, usar el historico de la historia en el punto de fin
        if sprintseleccionado.estados == 'FINALIZADO':
            print("Sprint finalizado")
            sprintActual2 = model_to_dict(sprintseleccionado)
            historias = sprintseleccionado.historias.order_by('id_historia')
            historiasList  = []
            for hist in historias:
                if hist.history.filter(Q(history_change_reason="fin_sprint") & Q(
                        history_date__lte=sprintActual2['fecha_final'] + timedelta(days=1))).exists():
                    x = hist.history.filter(Q(history_change_reason="fin_sprint") & Q(
                        history_date__lte=sprintActual2['fecha_final'] + timedelta(days=1))).last()
                    hist.nombre = x.nombre
                    hist.encargado = x.encargado
                    hist.descripcion = x.descripcion
                    hist.prioridad = x.prioridad
                    hist.horasEstimadas = x.horasEstimadas
                    hist.horas_dedicadas = x.horas_dedicadas
                    hist.estados = x.estados
                    historiasList.append(hist)
                else:
                    print("No existe")
        else:
            #El caso de que el sprint no este finalizado, es el actual
            historiasList = sprintseleccionado.historias.all()
        historiasSprint[sprintseleccionado.sprintNumber] = historiasList


    usuarioActual = auth.get_user(request)

    if (usuarioActual.is_superuser):
        fotodeusuario = None
    else:
        fotodeusuario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']

    proyectoActual = Proyecto.objects.get(id=id_proyecto)

    item = UserProyecto.objects.get(proyecto=proyectoActual, usuario=usuarioActual)


    if (item.rol_name != ''):
        rol = item.rol_name
    else:
        rol = ""



    context = {"Rol_de_usuario":rol,"ID_proyecto":id_proyecto,"proyecto":proyectoActual,"avatar":fotodeusuario,"usuario":usuarioActual,"historiasDict":historiasSprint }

    html = render_to_string("informe_US_AllSprints_pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; informe_US_AllSprints.pdf"

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)

    return response

def informe_US_ProductBacklog(request, id_proyecto):
    """
    Metodo para generar el reporte de todas las historias un proyecto

    :param request: Solicitud recibida
    :param id_proyecto: identificador del proyecto
    :return: Impresion de la historia con sus respectivos campos (nombre, encargado, descripcion, prioridad, horas Estimadas y dedicadas y su estado)
    """

    if Proyecto.objects.filter(id=id_proyecto).exists():
        proyecto = Proyecto.objects.get(id=id_proyecto)
    else:
        proyecto = None

    historias = Historia.objects.filter(proyecto=id_proyecto)
    historiasAlta = filter(lambda historia: historia.prioridad == 'ALTA', historias)
    historiasMedia = filter(lambda historia: historia.prioridad == 'MEDIA', historias)
    historiasBaja = filter(lambda historia: historia.prioridad == 'BAJA', historias)
    historia_list = []
    historia_list.extend(historiasAlta)
    historia_list.extend(historiasMedia)
    historia_list.extend(historiasBaja)

    context = {"historias":historia_list, "proyecto":proyecto}
    html = render_to_string("informe_US_ProductBacklog_pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; informe_US_Horas.pdf"

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)

    return response


def informe_BurndownChart(request,id_proyecto,id_sprint):
    """
    Metodo para Graficar el burndown chart en un gráfico de linea y exportarlo como pdf

    :param request: solicitud recibida
    :return: grafico de burndown chart
    """

    calendarioParaguay = Paraguay()
    proyecto = Proyecto.objects.get(id=id_proyecto)
    sprintActual = Sprint.objects.get(id=id_sprint)

    # 2- calculamos la capacidad del equipo
    capacidad_de_equipo = 0  #suma de las capacidades de los miembros del sprint
    desarrolladores = UserSprint.objects.filter(sprint=sprintActual)
    for desarrollador in desarrolladores:
        capacidad_de_equipo = capacidad_de_equipo + desarrollador.capacidad

    # 3- se extrae la lista de historias.
    #sprintActual2 = model_to_dict(sprintActual)
    #listaHistorias = sprintActual2['historias']
    listaHistorias = sprintActual.historias.all()
    cantidad_total_historia = len(listaHistorias)

    # Los miembros en forma de cadena para saber su estado
    total_horas_estimadas = 0
    miembrosSprint = []
    for hist in listaHistorias:
        total_horas_estimadas = total_horas_estimadas + hist.horasEstimadas
        try:
            #no entiendo
            lastlog = hist.encargado.last_login.strftime("%d/%b - %I:%M %p")
            miembro = f"{hist.encargado.email}\nUlt. activo : {lastlog}"
            if not miembro in miembrosSprint:
                miembrosSprint.append(miembro)
        except AttributeError:
            print(f"la historia {hist} aun no tiene encargado")
        # esto no se toca

    # 4 Se calcula la cantidad de dias del sprint
    #fechaInicio = sprintActual2['fecha_inicio']
    #fechaFin = sprintActual2['fecha_fin']
    fechaInicio = sprintActual.fecha_inicio
    fechaFin = sprintActual.fecha_fin


    dias_de_sprint = calendarioParaguay.get_working_days_delta(fechaInicio, fechaFin) + 1
    # 5 Se inicializan las variables que son necesarios para el line chart
    diasLaborales_py = []
    horasLaborales_Ideal = []
    horasLaborales_Real = []
    pasos = timedelta(days=1)

    diasLaborales_py.append("Inicio")
    # 6 Se genera la lista para el eje x del line chart
    while fechaInicio <= fechaFin:
        if calendarioParaguay.is_working_day(fechaInicio):
            diasLaborales_py.append(fechaInicio.strftime("%d-%b"))
        fechaInicio += pasos

    total_horas_dedicadas = 0

    # 8 Calculamos el efuerzo real.
    # Calcula la lista de esfuerzo real y lo guarda en el modelo
    #esto ha sido comentado
    #if(sprintActual.estados=="INICIADO"):
    #    calcularEsfuerzoReal(listaHistorias, sprintActual, diasLaborales_py, total_horas_estimadas)


    #horasLaborales_Ideal.append("Dia 0")
    #horasLaborales_Real.append("Dia 0")
    # SE PREPARAN LAS 2 LINEAS

    for i in sprintActual.horasLaboralesIdeal:
        horasLaborales_Ideal.append(str(i))

    # Se le da el formato actual para el line chart

    for i in sprintActual.horasLaboralesReal:
        horasLaborales_Real.append(str(i))

    usuarioActual = auth.get_user(request)
    if (usuarioActual.is_superuser):
        fotodeusuario = None
    else:
        fotodeusuario = SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']

    item = UserProyecto.objects.get(proyecto=proyecto, usuario=usuarioActual)


    if (item.rol_name != ''):
        rol = item.rol_name
    else:
        rol = ""


    context = {"usuario":usuarioActual,"Rol_de_usuario":rol,"avatar":fotodeusuario,"Sprint": sprintActual,
                       "Historias": listaHistorias,
                       "Total": cantidad_total_historia,
                       "diasLaborales": ','.join(diasLaborales_py),
                       "horasLaboralesIdeal": ','.join(horasLaborales_Ideal),
                       "horasLaboralesReal": ','.join(horasLaborales_Real),
                       "cantidadDias": dias_de_sprint,
                       "miembros": miembrosSprint,
                       "proyecto" : proyecto}
    html = render_to_string("informe_burndownChart_pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; informe_burndownChart.pdf"

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)

    return response