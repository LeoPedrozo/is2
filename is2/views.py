from django.http import HttpResponse
from django.db import models

from django.template import  Template,Context
from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount



#Hola mundo para probar django
def saludo(request):
    return render(request, "holaMundo.html", {"nombre": "Jose"})

def inicio(request):
    fotodeususario= SocialAccount.objects.filter(user=request.user)[0].extra_data['picture']
    return render(request, "sidenav.html", {"avatar":fotodeususario})

#Para acceder directamente a los archivos guardados en el directorio docs
#(Todavia no se ha implementado)
def documentaciones(request):
    return render(request,"html/index.html",{})

