from django.db import models
from userStory.models import Historia

"""
Definimos los estados de un Proyecto
"""
ESTADOS_CHOICES = [
    ('PENDIENTE','Pendiente'),
    ('INICIADO','Iniciado'),
    ('FINALIZADO','Finalizado'),
    ('CANCELADO','Cancelado'),
]

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


class Proyecto(models.Model):
    """
    Implementa la clase de Proyectos, almacena datos generales acerca del proyecto:
    nombre, estado, fecha, fecha entrega, fecha finalizacion e id sprints
    """
    nombre = models.CharField(max_length=100)
    descripcion=models.TextField(null=True,blank=True)
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, default='PENDIENTE')
    fecha = models.DateField(auto_now_add=True,blank=True)
    fecha_entrega = models.DateField()
    fecha_finalizacion = models.DateField(null=True)
    id_sprints = models.ManyToManyField(Sprint)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        """
        Metodo que retorna el nombre del proyecto actual

        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre

