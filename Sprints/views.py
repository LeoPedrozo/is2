from datetime import date, datetime

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
    newSprint = Sprint.objects.get(id=datosSprint['id'])
    newSprint.fecha_fin = datosSprint['fecha_fin']
    newSprint.save()
    return newSprint





def sprintActivoen(idProyecto):
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
    sprt = Sprint.objects.get(id=id)
    return sprt

# Vista subproceso de modificar, que sirve para no sobre cargar la vista de modificar. NO estoy usando
# recibe el diccionario que es request.session
# recibe le objeto proyecto


def guardarCamposdeSprint(request, sprint_seleccionado,id_proyecto):
    SprintActual = model_to_dict(sprint_seleccionado)

    request.session['id'] =  SprintActual['id']
    request.session['sprintNumber'] = SprintActual['sprintNumber']
    request.session['fecha_inicio'] = SprintActual['fecha_inicio'].strftime("%Y/%m/%d")
    request.session['fecha_fin'] = SprintActual['fecha_fin'].strftime("%Y/%m/%d")

    return True





