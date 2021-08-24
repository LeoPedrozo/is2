from django.shortcuts import render
from django.core.management import BaseCommand
from django.contrib.auth.models import Group , Permission
import logging
from django.contrib.auth.decorators import user_passes_test
# Modelos a los que se le aplicara los permisos
from userStory.models import Historia
from gestionUsuario.models import User,Equipo
from django.http import HttpRequest

from proyectos.models import Sprint, Proyecto



#Modelos = {
#    "Rol": "Scrum master",
#    "Historia": ["add", "delete"],
#    "Sprint" : ["change","view"]
#}

def gestionarPermisos(Modelos):
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


def agregarRol(user, grupo):
    #Agregar al usuario al grupo
    grupo.user_set.add(user)
    print("Adding {} to {}".format(user,grupo))


def group_required(mail,*group_names):
    """Requiere que el usuario pertenezca a almenos un grupo de los de la lista"""
    u = User.objects.filter(email__in=mail)
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')
