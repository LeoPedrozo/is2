from django.shortcuts import render
from django.forms import model_to_dict

from GestionPermisos.views import fabricarRol
from proyectos.models import Proyecto
from django.contrib.auth.models import Group
from gestionUsuario.models import User, UserProyecto

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


    scrum = {
        "RolName": "Scrum Master",
        "Proyecto": ["change","view"],
        "Historia": ["add","change","view","delete"],
        "Sprint" : ["add","change","view","delete"]
    }

    fabricarRol(scrum)

    desarrollador = {
        "RolName": "Desarrollador",
        "Historia": ["add", "change","view"],
        "Proyecto": ["view"],
        "Sprint": ["change", "view"]
    }
    fabricarRol(desarrollador)
    print("Asignando al proyecto")
    newP.roles_name.append('Scrum Master')
    newP.roles_name.append('Desarrollador')


    newP.save()
    return newP



def updateProyecto(datos):
    """
    Metodo que se ejecuta para actualizar los datos de un proyecto

    :param datos: informaciones referentes a los compos de datos de un proyecto
    :return: void
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

    :param project_id: identificador del proyecto
    :return: informacion completa del proyecto
    """

    print("EL id del proyecto es ", project_id)
    proyecto=Proyecto.objects.filter(id=project_id).latest('id')

   # proyecto = Proyecto.objects.get(nombre=project_id)
    return proyecto





def deleteProyecto(proyecto):
    """
    Metodo para la eliminacion de un proyecto

    :param proyecto: proyecto a eliminar
    :return: void
    """

    proyecto.delete()


#Esto puede generar problemas
def guardarCamposdeProyecto(request,proyecto_seleccionado):
    """
    Metodo que guarda todos lo campos de un proyecto

    :param request: Solicitud recibida
    :param usuarioActual: objeto del usuario actual
    :return: void
    """


    us=User.objects.all()
    usuarioslibres=[]
    for u in us:
        if( len( u.proyectos_asociados.filter(id=proyecto_seleccionado.id) ) == 0):
            usuarioslibres.append((u.email,u.email))

    proyecto=model_to_dict(proyecto_seleccionado)

    lista=UserProyecto.objects.filter(proyecto=proyecto_seleccionado)
    miembros=[]
    for l in lista:
        miembros.append((l.usuario.email,l.usuario.email))

    request.session['Proyecto']=proyecto['nombre']
    request.session['Descripcion']=proyecto['descripcion']
    request.session['estado']=proyecto['estado']
    request.session['fecha']=proyecto['fecha'].strftime("%Y/%m/%d")
    request.session['fecha_entrega'] = proyecto['fecha_entrega'].strftime("%Y/%m/%d")
    #request.session['fecha_finalizacion'] = proyecto['fecha_finalizacion'].strftime("%Y/%m/%d")
    request.session['miembros']=miembros
    request.session['usuarios']=usuarioslibres

    print(" Miembros : ", miembros)

    request.session['Proyecto_id']=proyecto['id']




