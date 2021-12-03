from django.contrib.postgres.fields import ArrayField
from django.db import models

from Sprints.models import Sprint
from userStory.models import Historia

"""
Definimos los estados de un Proyecto
"""
ESTADOS_CHOICES = [
    ('PENDIENTE','Pendiente'),
    ('INICIADO','Iniciado'),
    #('FINALIZADO','Finalizado'),
    #('CANCELADO','Cancelado'),
]

class Proyecto(models.Model):
    """
    Implementa la clase de Proyectos, almacena datos generales acerca del proyecto:
    nombre, estado, fecha, fecha entrega, fecha finalizacion e id sprints
    """

    nombre = models.CharField(max_length=100)
    descripcion=models.TextField(null=True,blank=False)
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES)
    fecha = models.DateField(blank=False)
    fecha_entrega = models.DateField(blank=False)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    id_sprints = models.ManyToManyField(Sprint, blank=True)
    #Los roles del proyecto.
    roles_name = ArrayField(models.CharField(max_length=30), default=list, blank=True)
    historial = ArrayField(models.TextField(), default=list, blank=True)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        """
        Metodo que retorna el nombre del proyecto actual

        :return: retorna el valor del campo nombre del objeto actual
        """

        return self.nombre

    def validate_test(self):
        """
        Metodo del modelo de Proyecto que retorna un booleano en caso
        que no se hayan completado todos los campos obligatorios en el proyecto.
        """

        if not self.nombre:
            return False
        if not self.descripcion:
            return False
        if not self.estado:
            return False
        if not self.fecha:
            return False
        if not self.fecha_entrega:
            return False
        return True