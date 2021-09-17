from django.db import models

# Create your models here.
from userStory.models import Historia


class Sprint(models.Model):
    """
    Clase de Sprint, almacena datos generales acerca de los sprint de un proyecto:
    identificador, Numero de Sprint, fecha de inicio, fecha fin e historias
    """
    id = models.AutoField(primary_key=True)
    sprintNumber = models.IntegerField()
    fecha_inicio = models.DateField(auto_now_add=True,blank=True)
    fecha_fin = models.DateField(auto_now_add=True,blank=True)
    historias = models.ManyToManyField(Historia,blank=True)


