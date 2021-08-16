from django.http import HttpResponse
from django.db import models

from django.template import  Template,Context
from django.shortcuts import render

#Hola mundo para probar django
def saludo(request):
    return render(request, "holaMundo.html", {"nombre": "Jose"})

def inicio(request):
    return render(request, "sidenav.html", {})

#Para acceder directamente a los archivos guardados en el directorio docs
#(Todavia no se ha implementado)
def documentaciones(request):
    return render(request,"html/index.html",{})