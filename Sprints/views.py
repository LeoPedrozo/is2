import datetime

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
    if datosSprint["historias"]:
        for historia in datosSprint["historias"]:
            #print(historia)
            #historia.estados="EN CURSO"
            historia.estados='PENDIENTE'
            historia.save()
            newSprint.historias.add(historia)
    proyecto = Proyecto.objects.get(id=datosSprint['idproyecto'])
    proyecto.id_sprints.add(newSprint)
    proyecto.save()

    return newSprint

def updateSprint(datosSprint):
    newSprint = Sprint.objects.get(id=datosSprint['id'])
    newSprint.fecha_fin = datosSprint['fecha_fin']
    newSprint.save()

    historias = datosSprint['historias']
    for historia in historias:
        # aca se puede modificar el campo de la histaria quitada del sprint
        historia.estados = None
        historia.save()




def sprintActivoen(idProyecto):
    proyecto = Proyecto.objects.get(id=idProyecto)

    ultimoSprint=proyecto.id_sprints.last()
    if ultimoSprint == None:
        return False
    fechaFinalizacion = ultimoSprint.fecha_fin
    fechaActual = datetime.date.today()

    if( fechaFinalizacion>fechaActual):
        return True
    else:
        return False




def getSprint(id):
    sprt = Sprint.objects.get(id=id)
    return sprt


# Vista subproceso de modificar, que sirve para no sobre cargar la vista de modificar. NO estoy usando
# recibe el diccionario que es request.session
# recibe le objeto proyecto


def guardarCamposdeSprint(request, proyectoActual):
    proyectoActual = model_to_dict(proyectoActual)
    listaSprint = proyectoActual['id_sprints']

    if len(listaSprint) != 0:
        SprintActual = listaSprint[-1]

        SprintActual = model_to_dict(SprintActual)

        print("el modelo del sprint es ")
        print(SprintActual)

        historias = SprintActual['historias']
        pk_list = []
        for historia in historias:
            h = model_to_dict(historia)
            pk_list.append(h['id_historia'])

        request.session['proyecto'] = proyectoActual['id']
        request.session['id'] = SprintActual['id']
        request.session['sprintNumber'] = SprintActual['sprintNumber']
        request.session['fecha_inicio'] = SprintActual['fecha_inicio'].strftime("%Y/%m/%d")
        request.session['fecha_fin'] = SprintActual['fecha_fin'].strftime("%Y/%m/%d")
        request.session['historias'] = pk_list

        return True
    else:
        return False
