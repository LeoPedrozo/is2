from django.db import models

# Create your models here.
from UserStory.models import Historia


class Sprint(models.Model):
    """
    Implementa la clase de Sprint, almacena datos generales acerca del los sprint de un proyecto:
    identificador, Numero de Sprint, fecha de inicio, fecha fin e historias
    """
    id = models.AutoField(primary_key=True)
    sprintNumber = models.IntegerField()
    fecha_inicio = models.DateField(auto_now_add=True,blank=True)
    fecha_fin = models.DateField(auto_now_add=True,blank=True)
    historias = models.ManyToManyField(Historia)

