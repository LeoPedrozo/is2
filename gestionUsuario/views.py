from django.core.mail import send_mail
from django.shortcuts import render
from gestionUsuario.models import User, UserProyecto


# Create your views here.

##una vista que reciba el id del proyecto recien creado y luego asociar ese id con los usuarios seleccionados tambien el formulario
##asociarmiembrosaproyecto
from is2 import settings


def asociarProyectoaUsuario( proyecto,correos):
    """Metodo para asociar un proyecto a un grupo de usuarios del sistema

    :param proyecto: proyecto que se quiere asociar
    :param miembros: lista de usuarios que van a ser asociados al proyecto
    :return: void
    """

    for correo in correos:

        u= User.objects.get(email=correo)
        u.proyecto=proyecto
        u.proyectos_asociados.add(proyecto)
        if UserProyecto.objects.filter(usuario=u, proyecto=proyecto).exists():
            a = UserProyecto.objects.get(usuario=u, proyecto=proyecto)
            a.rol_name = ''
            a.save()
        else:
            nuevo = UserProyecto(usuario=u, proyecto=proyecto, rol_name='')
            nuevo.save()
        u.save()
        """
        asunto = "Nuevo Proyecto!!"
        mensaje =  "Hola "+u.username+", has sido agregado a un nuevo proyecto\n\n Nombre del Proyecto: " +proyecto.nombre+"\n Fecha de creacion: "+str(proyecto.fecha)
        de = settings.EMAIL_HOST_USER
        destino = [u.email]
        send_mail(asunto,mensaje,de,destino)
        """


##No se si funca como deberia
def desasociarUsuariodeProyecto(proyecto,correos):
    """Metodo para desasociar a un grupo de usuarios de un proyecto

    :param miembro: usuarios que van a ser excluidos del proyecto
    :return: void
    """

    for correo in correos:
        u = User.objects.get(email=correo)
        #u.proyecto = None
        u.proyectos_asociados.remove(proyecto)

        print("lista de proyectos asociados Despues ", u.proyectos_asociados.all())
        if UserProyecto.objects.filter(usuario=u, proyecto=proyecto).exists():
            a = UserProyecto.objects.get(usuario=u, proyecto=proyecto)
            a.delete()

        u.save()






