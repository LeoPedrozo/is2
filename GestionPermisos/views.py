from django.shortcuts import render
from django.core.management import BaseCommand
from django.contrib.auth.models import Group , Permission
import logging
from django.contrib.auth.decorators import user_passes_test
# Modelos a los que se le aplicara los permisos
from UserStory.models import Historia
from gestionUsuario.models import User
from django.http import HttpRequest

from proyectos.models import Sprint, Proyecto



#Modelos = {
#    "Rol": "Scrum master",
#    "Historia": ["add", "delete"],
#    "Sprint" : ["change","view"]
#}

def fabricarRol(Modelos):
    """Gestion de permisos por medio de creaciones de grupos por medio de modelos previamente definidos con sus respectivos
        permisos, si el grupo es creado se imprime un mensaje de confirmacion sino se imprime un mensaje de error

    :param Modelos: (dict) listado de modelos de usuarios con sus permisos correspondientes
    :raises (str): Mensaje de error al asignar permisos a un grupo
    """
    #crear el grupo
    new_group, created = Group.objects.get_or_create(name=Modelos["Rol"])
    print("Creando el grupo "+Modelos["Rol"])

    Modelos.pop("Rol")

    #Asignar los permisos al grupo
    for modelo in Modelos:
        for app_model in Modelos[modelo]:
                    name = "Can {} {}".format( app_model, modelo)
                    print("Creating {}".format(name))
                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue
                    #Si pudo asignar, el carga ese permiso al grupo
                    new_group.permissions.add(model_add_perm)
    print("creado con exito")


def enlazar_Usuario_con_Rol(user, grupo):
    #Agregar al usuario al grupo
    """Agrega al usuario a un grupo

    :param user: usuario del sistema web
    :param grupo: grupo con sus permisos correspondientes
    """
    grupo.user_set.add(user)
    print("Adding {} to {}".format(user,grupo))



def registrar_usuario(user,state):
    grupo = Group.objects.get(name='registrado')
    users_in_group = grupo.user_set.all()

    if (state=='True'):
        if user in users_in_group :
            print("Ya existe por lo que no se agrega")
        else:
            print("se agrega")
            grupo.user_set.add(user)
    else:
        if user in users_in_group :
            grupo.user_set.remove(user)
            print("se remueve")
        else:
            print("No esta en el grupo por lo que no se necesrio hacer remove")


