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
    newSprint = Sprint(sprintNumber=datosSprint["sprintNumber"], fecha_inicio=datosSprint["fecha_inicio"],fecha_fin=datosSprint["fecha_fin"])
    newSprint.save()
    if datosSprint["historias"]:
        for historia in datosSprint["historias"]:
            print(historia)
            newSprint.historias.add(historia)
    proyecto=Proyecto.objects.get(id=datosSprint['idproyecto'])
    proyecto.id_sprints.add(newSprint)
    proyecto.save()

    return newSprint

def updateSprint(datosSprint):
    newSprint=Sprint.objects.filter(id=datosSprint['id'])
    newSprint.fecha_fin=datosSprint['fecha_fin']
    historias=datosSprint['historias']
    for historia in historias:
        #aca se puede modificar el campo de la histaria quitada del sprint
        historia.estados='PENDIENTE'
        historia.save()



def sprintActivoen(idProyecto):
    proyecto = Proyecto.objects.get(id=idProyecto)

    ultimoSprint=proyecto.id_sprints.last()

    fechaFinalizacion=ultimoSprint.fecha_fin
    fechaActual=  datetime.date.today()
    if( fechaFinalizacion>  fechaActual):
        return True
    else:
        return False







# Vista subproceso de modificar, que sirve para no sobre cargar la vista de modificar. NO estoy usando
# recibe el diccionario que es request.session
# recibe le objeto proyecto
def guardarCamposdeSprint(request, proyectoActual):
    proyectoActual = model_to_dict(proyectoActual)
    listaSprint = proyectoActual['id_sprints']
    SprintActual = listaSprint[-1]
    SprintActual = model_to_dict(SprintActual)
    historias = SprintActual['historias']
    pk_list = []
    for historia in historias:
        h = model_to_dict(historia)
        pk_list.append(h['id_historia'])

    request.session['proyecto'] = proyectoActual['id']
    request.session['id'] = SprintActual['id']
    request.session['sprintNumber'] = SprintActual['sprintNumber']
    request.session['historias'] = pk_list



#vista que funciona de modificar proyecto
"""
def modificarSprint(request):
    if request.method == "POST":
        formulario = modificarSprintForm(request.POST,request=request.session)
        if (formulario.is_valid()):
            # Acciones a realizar con el form
            datosSprint=formulario.cleaned_data
            updateSprint(formulario.cleaned_data)
            # Retornar mensaje de exito
            return render(request, "outputmodificarSprint.html", {"SprintModificado": datosSprint})
    else:
        usuarioActual = User.objects.get(username=request.user.username)
        if (usuarioActual.proyecto == None):
            return render(request, "Condicion_requerida.html", {"form": formulario})
        else:
            proyectoActual=usuarioActual.proyecto
            proyectoActual=model_to_dict(proyectoActual)
            listaSprint=proyectoActual['id_sprints']
            SprintActual=listaSprint[-1]##para estirar el ultimo elemento de la lista
            SprintActual=model_to_dict(SprintActual)
            historias=SprintActual['historias']
            pk_list=[]
            for historia in historias:
                h=model_to_dict(historia)
                pk_list.append(h['id_historia'])

            request.session['proyecto'] = usuarioActual.proyecto.id
            request.session['id'] = SprintActual['id']
            request.session['sprintNumber'] =SprintActual['sprintNumber']
            request.session['historias'] = pk_list

            formulario = modificarSprintForm(request=request.session)
            
            return render(request, "modificarSprint.html", {"form": formulario})

"""

