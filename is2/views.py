from django.http import HttpResponse
from django.db import models

from django.template import  Template,Context
from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required

from GestionPermisos.forms import crearRolForm, asignarRolForm
from GestionPermisos.views import gestionarPermisos,agregarRol
#Hola mundo para probar django
@login_required
def saludo(request):
    return render(request, "holaMundo.html", {"nombre": "Jose"})

def inicio(request):
    fotodeususario= SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']
    return render(request, "sidenav.html", {"avatar":fotodeususario})

#Para acceder directamente a los archivos guardados en el directorio docs
#(Todavia no se ha implementado)
def documentaciones(request):
    return render(request,"html/index.html",{})

def crearRol(request):
    if request.method == "POST":
        formulario = crearRolForm(request.POST)
        if(formulario.is_valid()):
            datosRol = formulario.cleaned_data
            #Acciones a realizar con el form
            gestionarPermisos(datosRol)

            #Retornar mensaje de exito
            return render(request,"holaMundo.html",{"configuracionDelRol":datosRol})
    else:
        formulario = crearRolForm()

    return render(request, "crearRol.html",{"form":formulario})



def asignarRol(request):
    if request.method == "POST":
        formulario = asignarRolForm(request.POST)
        if(formulario.is_valid()):
            datosRol=formulario.cleaned_data
            userdata = formulario.cleaned_data['Usuario']
            rol = formulario.cleaned_data['Roles']
            #Acciones a realizar con el form

            agregarRol(userdata,rol)

            #Retornar mensaje de exito
            return render(request,"outputAsignarRol.html",{"asignaciondeRol":datosRol})
    else:
        formulario = asignarRolForm()

    return render(request, "asignarRol.html",{"form":formulario})
