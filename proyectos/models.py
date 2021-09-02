from django.db import models
from userStory.models import Historia

ESTADOS_CHOICES = [
    ('PENDIENTE','Pendiente'),
    ('INICIADO','Iniciado'),
    ('FINALIZADO','Finalizado'),
    ('CANCELADO','Cancelado'),
]

class Sprint(models.Model):
    id = models.AutoField(primary_key=True)
    sprintNumber = models.IntegerField()
    fecha_inicio = models.DateField(auto_now_add=True,blank=True)
    fecha_fin = models.DateField(auto_now_add=True,blank=True)
    historias = models.ManyToManyField(Historia)


class Proyecto(models.Model):
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
        return self.nombre

