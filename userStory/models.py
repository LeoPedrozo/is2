from django.db import models
#from gestionUsuario.models import User

# Create your models here.
ESTADOS_CHOICES=[
    ('FINALIZADO','Finalizado'),
    ('PENDIENTE','Pendiente'),
    ('EN_CURSO','En Curso'),
    ('QUALITY_ASSURANCE','Quality Assurance'),
]
PRIORIDAD_CHOICES=[
    ('ALTA','Alta'),
    ('MEDIA','Media'),
    ('BAJA','Baja'),
]
class Historia(models.Model):
    id_historia = models.AutoField(primary_key = True)
    nombre=models.CharField(max_length=20)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES)
    fecha_creacion = models.DateField(auto_now_add=True)
    horasEstimadas = models.IntegerField
    estados = models.CharField(max_length=20, choices=ESTADOS_CHOICES)
    horas_dedicadas=models.IntegerField
    #encargado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Historia'
        verbose_name_plural = 'Historias'

    def __str__(self):
        return self.nombre

