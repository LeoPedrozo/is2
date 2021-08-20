from django.http import HttpResponse
from django.db import models

from django.template import  Template,Context
from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required

from GestionPermisos.forms import crearRolForm

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

            #Retornar mensaje de exito
            return render(request,"holaMundo.html",{"form1":datosRol})
    else:
        formulario = crearRolForm()

    return render(request, "crearRol.html",{"form":formulario})