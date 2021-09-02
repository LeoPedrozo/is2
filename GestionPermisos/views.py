from django.shortcuts import render
from django.core.management import BaseCommand
from django.contrib.auth.models import Group , Permission
import logging
from django.contrib.auth.decorators import user_passes_test
# Modelos a los que se le aplicara los permisos
from userStory.models import Historia
from gestionUsuario.models import User
from django.http import HttpRequest

from proyectos.models import Sprint, Proyecto



#Modelos = {
#    "Rol": "Scrum master",
#    "Historia": ["add", "delete"],
#    "Sprint" : ["change","view"]
#}

def fabricarRol(Modelos):
    # Crear el grupo
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


def enlazar_Ususario_con_Rol(user, grupo):
    #Agregar al usuario al grupo
    grupo.user_set.add(user)
    print("Adding {} to {}".format(user,grupo))

