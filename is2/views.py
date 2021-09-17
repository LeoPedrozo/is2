from django.forms import model_to_dict
from django.http import HttpResponse
from django.db import models

from django.template import  Template,Context
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from GestionPermisos.forms import crearRolForm, asignarRolForm, registroDeUsuariosForm, seleccionarRolForm, \
    modificarRolForm
from GestionPermisos.views import fabricarRol, enlazar_Usuario_con_Rol, registrar_usuario, removerRol
from Sprints.views import nuevoSprint
from gestionUsuario.models import User
from gestionUsuario.views import asociarProyectoaUsuario
from proyectos.views import nuevoProyecto, getProyecto, updateProyecto
from proyectos.forms import crearproyectoForm, modificarproyectoForm
from django.contrib.auth.decorators import user_passes_test
from Sprints.forms import crearSprintForm
from userStory.forms import crearHistoriaForm
from userStory.models import Historia
from userStory.views import nuevaHistoria

#Hola mundo para probar django
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


#Para acceder directamente a los archivos guardados en el directorio docs
#(Todavia no se ha implementado)
def documentaciones(request):
    """
    Metodo para acceder directamente a los archivos referentes a la documentacion del sistema

    :param request: consulta recibida
    :return: respuesta: de redireccionamiento
    """
    return render(request,"html/index.html",{})


##VISTAS RELACIONADAS AL MANEJO DE ROL

def crearRol(request):
    """
    Metodo para la creacion de roles del sistema

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR ROL
    """
    if request.method == "POST":
        formulario = crearRolForm(request.POST)
        if(formulario.is_valid()):
            datosRol = formulario.cleaned_data

            print(formulario.cleaned_data)

            nombreRol = formulario.cleaned_data["RolName"]
            historia=formulario.cleaned_data["Historia"]
            proyecto=formulario.cleaned_data["Proyecto"]
            sprint=formulario.cleaned_data["Sprint"]

            #Acciones a realizar con el form
            fabricarRol(datosRol)
            #Retornar mensaje de exito
            return render(request, "rolCreado.html", {"nombreRol":nombreRol,"historia":historia,"proyecto":proyecto,"sprint":sprint})
    else:
        formulario = crearRolForm()

    return render(request, "crearRol.html",{"form":formulario})


def asignarRol(request):
    """
    Metodo para la asignacion de roles a los usuarios del sistema

    :param request: solicitud recibida
    :return: respuesta: a la solicitud de ASIGNAR ROL
    """
    if request.method == "POST":
        formulario = asignarRolForm(request.POST)
        if(formulario.is_valid()):
            datosRol=formulario.cleaned_data
            userdata = formulario.cleaned_data['Usuario']
            rol = formulario.cleaned_data['Roles']
            #Acciones a realizar con el form

            enlazar_Usuario_con_Rol(userdata,rol)

            #Retornar mensaje de exito
            return render(request,"outputAsignarRol.html",{"asignaciondeRol":datosRol})
    else:
        formulario = asignarRolForm()

    return render(request, "asignarRol.html",{"form":formulario})


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


#modificar Rol 1
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

            request.session['RolSeleccionado']=RolSeleccionado.name

            modeloRol=model_to_dict(RolSeleccionado)

            print("Modelo Rol: ")
            print(modeloRol)

            getPermisos(request,modeloRol['permissions'])


            return redirect(modificarRol)
    else:
        formulario = seleccionarRolForm()

    return render(request, "seleccionarRol.html", {"form": formulario})

#modificar Rol 2
def modificarRol(request):
    """
    Metodo para la modificacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR PROYECTO
    """
    if request.method == "POST":


        formulario = modificarRolForm(request.POST)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosdeRol=formulario.cleaned_data
            # Retornar mensaje de exito
            return render(request, "outputmodificarProyecto.html", {"proyectoCreado": datosdeRol})
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
        if(formulario.is_valid()):
            datos=formulario.cleaned_data
            userdata = formulario.cleaned_data['Usuario']
            estado = formulario.cleaned_data['Habilitado']
            #Acciones a realizar con el form
            registrar_usuario(userdata,estado)

            #Retornar mensaje de exito
            return render(request,"outputRegistrarUsuario.html",{"usuario":datos})
    else:
        formulario = registroDeUsuariosForm()

    return render(request, "RegistrarUsuario.html", {"form":formulario})




#VISTAS RELACIONADAS AL MANEJO DE PROYECTOS

def crearProyecto(request):
    """
    Metodo para la creacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR PROYECTO
    """
    if request.method == "POST":
        ##instance = User.objects.filter(user=request.user).first()

        formulario = crearproyectoForm(request.POST,request=request)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosProyecto=formulario.cleaned_data
            miembros=formulario.cleaned_data["miembros"]
            nuevoProyecto(formulario.cleaned_data)
            proyecto = getProyecto(formulario.cleaned_data['nombre'])
            asociarProyectoaUsuario(proyecto,miembros)
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
    if request.method == "POST":
        ##instance = User.objects.filter(user=request.user).first()

        formulario = modificarproyectoForm(request.POST,)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosProyecto=formulario.cleaned_data
            miembros = formulario.cleaned_data["miembros"]

            updateProyecto(formulario.cleaned_data)

            proyecto = getProyecto(formulario.cleaned_data['nombre'])

            asociarProyectoaUsuario(proyecto,miembros)

            # Retornar mensaje de exito
            return render(request, "outputmodificarProyecto.html", {"proyectoCreado": datosProyecto})
    else:
        formulario = modificarproyectoForm(request=request)

    return render(request, "modificarProyecto.html", {"form": formulario})




##Metodo bastante horrible pero que hace su funcion.
def getPermisos(request,listaPermisos):
    """
    Metodo de gestion y asignacion de permisos para los usuarios del sistema

    :param request: solicitud recibida
    :param listaPermisos: lista de permisos a ser distribuidos
    :return: respuesta a la solicitud de ejecucion recibida para el metodo GETPERMISOS
    """
    listaProyecto=[]
    listaHistoria=[]
    listaSprint=[]


    for objeto_permiso in listaPermisos:
         lista =(str(objeto_permiso)).split("|")

         categoria=lista[1]
         permiso=lista[2]

         if(permiso.find(' Can add Proyecto')>=0):
             listaProyecto.append("add")
         if(permiso.find(' Can change Proyecto')>=0):
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


    request.session['Proyecto']=listaProyecto
    request.session['Historia']=listaHistoria
    request.session['Sprint']=listaSprint





def crearSprint(request):
    """
    Metodo para la creacion de proyectos

    :param request: solicitud recibida
    :return: respuesta a la solicitud de CREAR PROYECTO
    """
    if request.method == "POST":
        ##instance = User.objects.filter(user=request.user).first()

        formulario = crearSprintForm(request.POST,request=request)
        if (formulario.is_valid()):
            # Acciones a realizar con el form

            datosSprint=formulario.cleaned_data
            nuevoSprint(datosSprint)


            #datosProyecto=formulario.cleaned_data
            #miembros=formulario.cleaned_data["miembros"]
            #nuevoProyecto(formulario.cleaned_data)
            #proyecto = getProyecto(formulario.cleaned_data['nombre'])
            #asociarProyectoaUsuario(proyecto,miembros)
            # Retornar mensaje de exito
            return render(request, "outputCrearSprint.html", {"sprintCreado": datosSprint})
    else:
          formulario = crearSprintForm(request=request)

    return render(request, "crearSprint.html", {"form": formulario})


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

    return render(request, "AvatarContent.html", {"miembros": usuarios,"fotos": fotos})


def crearHistoria(request):
    """
    Metodo que es ejecutado para crear un user story

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de crearHistoria
    """
    if request.method == "POST":
        formulario = crearHistoriaForm(request.POST)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosHistoria=formulario.cleaned_data

            nuevaHistoria(datosHistoria)
            # Retornar mensaje de exito
            return render(request, "outputCrearUserStory.html", {"historiaCreado": datosHistoria})
    else:
        formulario = crearHistoriaForm()

    return render(request, "crearUserStory.html", {"form": formulario})



def verHistorias(request):
    """
    Metodo que es ejecutado para mostrar los miembros de un proyecto

    :param request: consulta recibida
    :return: respuesta a la solicitud de ejecucion de verMiembros
    """
    historias = Historia.objects.all()
    print(historias)

    return render(request, "HistoriaContent.html", {"historias": historias})