from django.shortcuts import render
from gestionUsuario.models import User
# Create your views here.

##una vista que reciba el id del proyecto recien creado y luego asociar ese id con los usuarios seleccionados tambien el formulario
##asociarmiembrosaproyecto

def asociarProyectoaUsuario( proyecto,miembros):
    for miembro in miembros:
        u= User.objects.get(username=miembro)
        u.proyecto=proyecto
        u.save()


##No se si funca como deberia
def desasociarUsuariodeProyecto(miembro):
    u = User.objects.get(username=miembro)
    ##u.proyecto.objects.delete(nombre=project_name)
    u.proyecto.delete()
    u.save()






