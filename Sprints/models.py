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
    fecha_inicio = models.DateField(blank=False)
    fecha_fin = models.DateField(blank=False)
    historias = models.ManyToManyField(Historia,blank=True)


    def validate_test(self):
        """
        Metodo del modelo de Sprint que retorna un booleano en caso
        que no se hayan completado todos los campos obligatorios en el sprint.
        """

        if not self.sprintNumber:
            return False
        if not self.fecha_inicio:
            return False
        if not self.fecha_fin:
            return False
        return True