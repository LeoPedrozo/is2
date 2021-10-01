from django.shortcuts import render

# Create your views here.
from userStory.models import Historia


def nuevaHistoria(datosHistoria):
    newH=Historia(nombre=datosHistoria["nombre"],
                  descripcion=datosHistoria["descripcion"],
                  prioridad=datosHistoria["prioridad"],
                  fecha_creacion=datosHistoria["fecha_creacion"],#sera que se le asigna correctamente?
                  horasEstimadas=datosHistoria["horasEstimadas"],
                  estados='',
                  horas_dedicadas=datosHistoria["horas_dedicadas"],
                  proyecto=datosHistoria['proyecto'])
    newH.save()

#modificacion en general
def updateHistoria(datosHistoria):
    oldH = Historia.objects.get(id_historia=datosHistoria['id_historia'])
    oldH.nombre=datosHistoria["nombre"]
    oldH.descripcion=datosHistoria["descripcion"]
    oldH.prioridad=datosHistoria["prioridad"]
    #oldH.fecha_creacion = datosHistoria["fecha_creacion"]
    oldH.horasEstimadas=datosHistoria["horasEstimadas"]

    oldH.horas_dedicadas=datosHistoria["horas_dedicadas"]
    oldH.save()


