from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
from proyectos.models import Proyecto
from userStory.models import Historia
from simple_history import register

class User(AbstractUser):
    """
    Usuario que tiene admitido realizar loggeo en el sistema
    """

    #Proyecto actual del usuario
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True, blank=True)
    #Todos los proyectos a los que esta asociado el usuario
    proyectos_asociados=models.ManyToManyField(Proyecto,blank=True, related_name='proyectos')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

register(User)


# Equipos para evitar agregar individualmente los usuarios al proyecto
#class Equipo(models.Model):
#    """ Asignar equipos de trabajo a proyectos de manera a evitar agregarlos individualmente"""
#    nombre = models.CharField(max_length=50)
#    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True, blank=True)
#    users = models.ManyToManyField(User)
#
 #   def __str__(self):
#            return f"El equipo {self.nombre} esta asignado al proyecto {self.proyecto}"




class UserProyecto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True, blank=True)
    #Esta lista representa el rol del usuario_id en el proyecto_id
    rol_name = models.CharField(blank=True, max_length=30)
