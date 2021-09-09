from django.http import HttpResponse
from django.db import models

from django.template import  Template,Context
from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from GestionPermisos.forms import crearRolForm, asignarRolForm, registroDeUsuariosForm
from GestionPermisos.views import fabricarRol, enlazar_Usuario_con_Rol, registrar_usuario
from gestionUsuario.models import User
from gestionUsuario.views import asociarProyectoaUsuario
from proyectos.views import nuevoProyecto, getIdProyecto, updateProyecto
from proyectos.forms import crearproyectoForm, modificarproyectoForm
from django.contrib.auth.decorators import user_passes_test

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
            #Acciones a realizar con el form
            fabricarRol(datosRol)

            #Retornar mensaje de exito
            return render(request, "rolCreado.html", {"configuracionDelRol":datosRol})
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
            proyecto = getIdProyecto(formulario.cleaned_data['nombre'])
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

        formulario = modificarproyectoForm(request.POST,request=request)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosProyecto=formulario.cleaned_data
            miembros = formulario.cleaned_data["miembros"]

            updateProyecto(formulario.cleaned_data)

            proyecto = getIdProyecto(formulario.cleaned_data['nombre'])

            asociarProyectoaUsuario(proyecto,miembros)

            # Retornar mensaje de exito
            return render(request, "outputmodificarProyecto.html", {"proyectoCreado": datosProyecto})
    else:
        formulario = modificarproyectoForm(request=request)

    return render(request, "modificarProyecto.html", {"form": formulario})



