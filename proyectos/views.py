from django.shortcuts import render

from proyectos.models import Proyecto
# Create your views here.


## vista para crear un proyecto-> agregar a la tabla


def nuevoProyecto(datos):
    newP= Proyecto(nombre = datos['nombre'],estado = datos['estado'],descripcion = datos['descripcion'],fecha = datos['fecha'],fecha_entrega =datos['fecha_entrega'],fecha_finalizacion=None)
    newP.save()




