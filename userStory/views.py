from django.shortcuts import render

# Create your views here.
from userStory.models import Historia


def nuevaHistoria(datosHistoria):
    newH=Historia(nombre=datosHistoria["nombre"],descripcion=datosHistoria["descripcion"],prioridad=datosHistoria["prioridad"],fecha_creacion=datosHistoria["fecha_creacion"],horasEstimadas=datosHistoria["horasEstimadas"],estados=datosHistoria["estados"],horas_dedicadas=datosHistoria["horas_dedicadas"])
    newH.save()
