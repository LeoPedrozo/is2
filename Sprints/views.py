from datetime import date, datetime, timedelta

from django.forms import model_to_dict
from django.shortcuts import render

# Create your views here.
from Sprints.models import Sprint
from proyectos.models import Proyecto


def nuevoSprint(datosSprint):
    """Metodo que se ejecuta para visualizar la informacion de un nuevo sprint

    :param datosSprint: datos de un sprint
    :return: respuesta a la solicitud de NUEVO SPRINT
    """

    newSprint = Sprint(sprintNumber=datosSprint["sprintNumber"], fecha_inicio=datosSprint["fecha_inicio"],
                       fecha_fin=datosSprint["fecha_fin"])
    newSprint.save()
    proyecto = Proyecto.objects.get(id=datosSprint['idproyecto'])
    proyecto.id_sprints.add(newSprint)
    proyecto.save()
    return newSprint

def updateSprint(datosSprint):
    """
    Metodo que se ejecuta para actualizar los datos de un sprint

    :param datos: informaciones referentes a los compos de datos de un sprint
    :return: void
    """
    newSprint = Sprint.objects.get(id=datosSprint['id'])
    newSprint.fecha_inicio=datosSprint['fecha_inicio']
    newSprint.fecha_fin = datosSprint['fecha_fin']
    newSprint.save()
    return newSprint


def sprintActivoen(idProyecto):
    """
    Metodo que verifica si hay o no un sprint activo en el proyecto

    :param idProyecto: Identificador de proyecto
    :return: boolean
    """

    proyecto = Proyecto.objects.get(id=idProyecto)
    #proyecto = Proyecto.objects.get(id=idProyecto)
    proyecto= Proyecto
    ultimoSprint=proyecto.id_sprints.last()
    if ultimoSprint == None:
        return False
    fechaFinalizacion = ultimoSprint.fecha_fin
    fechaActual = datetime.date.today()

    if( fechaFinalizacion>fechaActual):
        return True
    else:
        return False


#dado un id te retorna el sprint
def getSprint(id):
    """
    Metodo que retorna el objeto sprint dado el identificador

    :param id: identificador de sprint
    :return: objeto sprint
    """

    sprt = Sprint.objects.get(id=id)
    return sprt

# Vista subproceso de modificar, que sirve para no sobre cargar la vista de modificar. NO estoy usando
# recibe el diccionario que es request.session
# recibe le objeto proyecto


def guardarCamposdeSprint(request, sprint_seleccionado,proyecto):
    """
    Metodo que se ejecuta para guardar los campos de un Sprint

    :param request: Solicitud recibida
    :param sprint_seleccionado: sprint que se desea guardar
    :param id_proyecto: identificador del proyecto al cual pertenece
    :return: (boolean) Confirmacion de la accion realizada
    """

    SprintActual = model_to_dict(sprint_seleccionado)

    request.session['id'] =  SprintActual['id']
    request.session['sprintNumber'] = SprintActual['sprintNumber']
    request.session['fecha_inicio'] = SprintActual['fecha_inicio'].strftime("%Y/%m/%d")
    request.session['fecha_fin'] = SprintActual['fecha_fin'].strftime("%Y/%m/%d")

    return True





