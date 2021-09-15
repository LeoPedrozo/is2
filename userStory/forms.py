from django import forms
from django.contrib.auth.models import Group
from gestionUsuario.models import User
import datetime

class crearHistoriaForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la creacion de un proyecto
    """
    # overwrite __init__
   # def __init__(self, *args, **kwargs):
        #self.request = kwargs.pop("request")  # store value of request
        ##super(crearproyectoForm,self).__init__(*args, **kwargs)
        #self.fields['creador'].initial=self.request.user.username

    ESTADOS_CHOICES = [
        ('FINALIZADO', 'Finalizado'),
        ('PENDIENTE', 'Pendiente'),
        ('EN_CURSO', 'En Curso'),
        ('QUALITY_ASSURANCE', 'Quality Assurance'),
    ]

    """
    Definimos la prioridad de un userStory
    """
    PRIORIDAD_CHOICES = [
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
    ]
    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea)
    prioridad = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=PRIORIDAD_CHOICES)
    fecha_creacion = forms.DateField(initial=datetime.date.today,disabled=True,label="Fecha de Creacion")
    horasEstimadas = forms.IntegerField(initial=0)
    estados = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=ESTADOS_CHOICES)
    horas_dedicadas = forms.IntegerField(initial=0)

