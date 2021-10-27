from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from userStory.models import Historia

"""
Definimos los posibles estados del Sprint
"""
ESTADOS_CHOICES=[
    ('PLANNING','Planning'),
    ('INICIADO','Iniciado'),
    ('FINALIZADO','Finalizado'),
]

class Sprint(models.Model):
    """
    Clase de Sprint, almacena datos generales acerca de los sprint de un proyecto:
    identificador, Numero de Sprint, fecha de inicio, fecha fin e historias
    """
    id = models.AutoField(primary_key=True)
    sprintNumber = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_final= models.DateField(null=True)
    historias = models.ManyToManyField(Historia,blank=True)
    estados = models.CharField(max_length=20, choices=ESTADOS_CHOICES,default='PLANNING')
    #El Sprint es verificado, cuando el Scrum realiza todos los QA de las historias y confirma
    verificado = models.BooleanField(default=False)

    ##Esto lo agrege yo por que estoy re loco
    horasLaboralesReal = ArrayField(models.IntegerField(), default=list, blank=True)
    horasLaboralesIdeal = ArrayField(models.IntegerField(), default=list, blank=True)

    def validate_test(self):
        """
        Metodo del modelo de Sprint que retorna un booleano en caso
        que se hayan completado o no todos los campos obligatorios en el sprint.
        """
        if not self.sprintNumber:
            return False
        if not self.fecha_inicio:
            return False
        if not self.fecha_fin:
            return False
        return True