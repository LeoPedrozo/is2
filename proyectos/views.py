from django.shortcuts import render
from django.forms import model_to_dict
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
    proyecto=Proyecto.objects.get(id=datos['id'])
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
    print("EL id del proyecto es ", project_id)
    proyecto=Proyecto.objects.filter(id=project_id).latest('id')

   # proyecto = Proyecto.objects.get(nombre=project_id)
    return proyecto





def deleteProyecto(proyecto):
    proyecto.delete()


#Esto puede generar problemas
def guardarCamposdeProyecto(request,usuarioActual):

    usuario=model_to_dict(usuarioActual)
    proyecto=model_to_dict(usuarioActual.proyecto)
    print("usuario = ", usuario)
    print("proyecto", proyecto)

    request.session['creador']=usuario['username']
    request.session['Proyecto']=proyecto['nombre']
    request.session['Descripcion']=proyecto['descripcion']
    request.session['estado']=proyecto['estado']
    request.session['fecha']=proyecto['fecha'].strftime("%Y/%m/%d")
    request.session['fecha_entrega'] = proyecto['fecha_entrega'].strftime("%Y/%m/%d")
    #request.session['fecha_finalizacion'] = proyecto['fecha_finalizacion'].strftime("%Y/%m/%d")
    request.session['Proyecto_id']=proyecto['id']




