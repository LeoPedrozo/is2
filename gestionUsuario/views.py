from django.shortcuts import render
from gestionUsuario.models import User
# Create your views here.

##una vista que reciba el id del proyecto recien creado y luego asociar ese id con los usuarios seleccionados tambien el formulario
##asociarmiembrosaproyecto

def asociarProyectoaUsuario( proyecto,miembros):
    """Metodo para asociar un proyecto a un grupo de usuarios del sistema

    :param proyecto: proyecto que se quiere asociar
    :param miembros: lista de usuarios que van a ser asociados al proyecto
    :return: void
    """
    for miembro in miembros:
        u= User.objects.get(username=miembro)
        u.proyecto=proyecto
        u.save()


##No se si funca como deberia
def desasociarUsuariodeProyecto(miembros):
    """Metodo para desasociar a un usuario de un proyecto

    :param miembro: usuario que va ser excluido del proyecto
    :return: void
    """

    for miembro in miembros:
        u = User.objects.get(username=miembro)
        u.proyecto = None
        u.save()






