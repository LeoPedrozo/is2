
from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.

"""
Definimos los estados de un userStory
"""
ESTADOS_CHOICES=[
    ('FINALIZADO','Finalizado'),
    ('PENDIENTE','Pendiente'),
    ('EN_CURSO','En Curso'),
    ('QUALITY_ASSURANCE','Quality Assurance'),
    ('RELEASE','Release')
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
    identificador, nombre, descripcion,comentarios, prioridad, fecha de creacion, horas estimadas estados, horas dedicadas y comentario extra
    """
    id_historia = models.AutoField(primary_key = True)
    nombre=models.CharField(max_length=50)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES)
    fecha_creacion = models.DateField(auto_now_add=True)
    horasEstimadas = models.IntegerField(default=0)
    estados = models.CharField(max_length=20, choices=ESTADOS_CHOICES, blank=True)
    horas_dedicadas=models.IntegerField(default=0, blank=True)
    proyecto=models.ForeignKey(to='proyectos.Proyecto', on_delete=models.SET_NULL,null=True,blank=True)

    #Jose= esto lo agrego por que estoy re loco
    encargado=models.ForeignKey(to='gestionUsuario.User', on_delete=models.SET_NULL,null=True,blank=True)

    comentarios=models.TextField(default='')
    extraData = models.TextField(default='')
    history = HistoricalRecords(user_model='gestionUsuario.User')

    class Meta:
        verbose_name = 'Historia'
        verbose_name_plural = 'Historias'

    def __str__(self):
        """
        Metodo que retorna el nombre del userStory actual

        :return: retorna el valor del campo nombre del objeto actual
        """
        return self.nombre

    def validate_test(self):
        """
        Metodo del modelo de Sprint que retorna un booleano en caso
        que se hayan completado o no todos los campos obligatorios en el User Story.
        """
        if not self.nombre:
            return False
        if not self.descripcion:
            return False
        if not self.prioridad:
            return False
        if not self.fecha_creacion:
            return False
        if not self.horasEstimadas:
            return False
        return True

    @property
    def _history_user(self):
        return self.encargado

    @_history_user.setter
    def _history_user(self, value):
        self.encargado = value