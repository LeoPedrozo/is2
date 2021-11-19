from django.shortcuts import render

# Create your views here.
from userStory.models import Historia


def nuevaHistoria(datosHistoria):
    """
    Metodo que se ejecuta para visualizar los datos de una nueva historia creada

    :param datos: informaciones referentes a los campos de datos de una historia
    :return: info de la nueva historia
    """
    newH=Historia(nombre=datosHistoria["nombre"],
                  descripcion=datosHistoria["descripcion"],
                  prioridad=datosHistoria["prioridad"],
                  fecha_creacion=datosHistoria["fecha_creacion"],#sera que se le asigna correctamente?
                  #horasEstimadas=datosHistoria["horasEstimadas"],
                  horasEstimadas=0,
                  estados='',
                  horas_dedicadas=0,
                  proyecto=datosHistoria['proyecto'])
    newH.save()

#modificacion en general
def updateHistoria(datosHistoria):
    """
    Method que se ejecuta para actualizar los datos de una nueva historia creada

    :param datos: informaciones referentes a los compos de datos de una historia
    :return: info de la historia actualizada
    """
    oldH = Historia.objects.get(id_historia=datosHistoria['id_historia'])
    oldH.nombre=datosHistoria["nombre"]
    oldH.descripcion=datosHistoria["descripcion"]
    oldH.prioridad=datosHistoria["prioridad"]
    #oldH.fecha_creacion = datosHistoria["fecha_creacion"]
    #oldH.horasEstimadas=datosHistoria["horasEstimadas"]
    #oldH.horas_dedicadas=datosHistoria["horas_dedicadas"]
    oldH.save()

def asignarEncargado(Historia, encargado ):
    """
    Metodo para la asignacion de encargado a una historia

    :param Historia: Historia
    :param encargado: Encargado a ser asignado a la historia
    :return: void
    """
    for historia in Historia:
        if historia.encargado is None:
            historia.encargado = encargado
            historia.save()
        else:
            print("La historia ya posee como encargado a : ",historia.encargado)
            print("Asignando de todas formas...")
            historia.encargado = encargado
            historia.save()


