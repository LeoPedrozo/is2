from django.shortcuts import render

from proyectos.models import Proyecto
# Create your views here.


## vista para crear un proyecto-> agregar a la tabla


def nuevoProyecto(datos):
    """
    Metodo que se ejecuta para visualizar los datos de un nuevo proyecto creado
    :param datos: informaciones referentes a los compos de datos de un proyecto
    :return: info del nuevo proyecto
    """
    newP= Proyecto(nombre = datos['nombre'],estado = datos['estado'],descripcion = datos['descripcion'],fecha = datos['fecha'],fecha_entrega =datos['fecha_entrega'],fecha_finalizacion=None)
    newP.save()




