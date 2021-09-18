from django.shortcuts import render

from proyectos.models import Proyecto
# Create your views here.


## vista para crear un proyecto-> agregar a la tabla


def nuevoProyecto(datos):
    """
    Metodo que se ejecuta para visualizar los datos de un nuevo proyecto creado

    :param datos: informaciones referentes a los campos de datos de un proyecto
    :return: info del nuevo proyecto
    """
    newP= Proyecto(nombre = datos['nombre'],estado = datos['estado'],
                   descripcion = datos['descripcion'],fecha = datos['fecha'],
                   fecha_entrega =datos['fecha_entrega'],fecha_finalizacion=None)
    newP.save()
    return newP



def updateProyecto(datos):
    """
    Metodo que se ejecuta para actualizar los datos de un nuevo proyecto creado

    :param datos: informaciones referentes a los compos de datos de un proyecto
    :return: info del nuevo proyecto
    """
    proyecto=Proyecto.objects.get(nombre=datos['nombre'])
    proyecto.nombre=datos['nombre']
    proyecto.estado = datos['estado']
    proyecto.descripcion = datos['descripcion']
    proyecto.fecha = datos['fecha']
    proyecto.fecha_entrega =datos['fecha_entrega']
    proyecto.fecha_finalizacion=None
    proyecto.save()




def getProyecto(project_id):
    """
    Metodo para obtener todos los datos de un proyecto

    :param project_name: nombre del proyecto
    :return: informacion completa del proyecto
    """
    #proyecto=Proyecto.objects.get(id=project_id)
    proyecto = Proyecto.objects.get(nombre=project_id)
    return proyecto





def deleteProyecto(proyecto):
    proyecto.delete()


## la vista que reciba el id de un proyecto()
    ##retorne la lista.
