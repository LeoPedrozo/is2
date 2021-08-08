from django.http import HttpResponse

from django.template import  Template,Context
from django.shortcuts import render
def saludo(request):
    return render(request,"menuprincipal.html",{"nombre":"Leo"})

