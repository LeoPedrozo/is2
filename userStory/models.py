
from django.db import models
#from gestionUsuario.models import User

# Create your models here.

"""
Definimos los estados de un userStory
"""
ESTADOS_CHOICES=[
    ('FINALIZADO','Finalizado'),
    ('PENDIENTE','Pendiente'),
    ('EN_CURSO','En Curso'),
    ('QUALITY_ASSURANCE','Quality Assurance'),
]

"""
Definimos la prioridad de un userStory
"""
PRIORIDAD_CHOICES=[
    ('ALTA','Alta'),
    ('MEDIA','Media'),
    ('BAJA','Baja'),
]

class Historia(models.Model):
    """
    Implementa la clase de Historias de Usuario, almacena datos generales acerca del userStory:
    identificador, nombre, descripcion, prioridad, fecha de creacion, horas estimadas estados y horas dedicadas
    """
    id_historia = models.AutoField(primary_key = True)
    nombre=models.CharField(max_length=20)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES)
    fecha_creacion = models.DateField(auto_now_add=True)
    horasEstimadas = models.IntegerField(default=0)
    estados = models.CharField(max_length=20, choices=ESTADOS_CHOICES)
    horas_dedicadas=models.IntegerField(default=0)
    proyecto=models.ForeignKey(to='proyectos.Proyecto', on_delete=models.SET_NULL,null=True,blank=True)

    class Meta:
        verbose_name = 'Historia'
        verbose_name_plural = 'Historias'

    def __str__(self):
        """
        Metodo que retorna el nombre del userStory actual

        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre

