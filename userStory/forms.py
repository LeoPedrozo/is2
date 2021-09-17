from django import forms
from django.contrib.auth.models import Group
from gestionUsuario.models import User
import datetime

from userStory.models import Historia


class seleccionarHistoriaForm(forms.Form):
    """
      Implementa la clase para ejecutar un formulario de solicitud para la seleccion de la historia que se desea modificar
    """
    def __init__(self, *args, **kwargs):
        self.proyecto = kwargs.pop('proyecto')  # store value of request
        super(seleccionarHistoriaForm, self).__init__(*args, **kwargs)
        self.fields['Historia'].queryset=Historia.objects.filter(proyecto_id=self.proyecto)

    Historia = forms.ModelChoiceField(queryset=Historia.objects.all(),initial=0,label="Selecciona la historia")

class modificarHistoriaForm(forms.Form):
    """
      Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la modificacion de una historia de usuario
    """
    def __init__(self, *args, **kwargs):
        self.datosHistoria = kwargs.pop("datosdelaHistoria")  # store value of request
        super(modificarHistoriaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].initial = self.datosHistoria['nombre']
        self.fields['descripcion'].initial = self.datosHistoria['descripcion']
        self.fields['prioridad'].initial = self.datosHistoria['prioridad']#este tambien
        self.fields['fecha_creacion'].initial = self.datosHistoria['fecha_creacion']
        self.fields['horasEstimadas'].initial = self.datosHistoria['horasEstimadas']
        self.fields['estados'].initial = self.datosHistoria['estados']#este es especial
        self.fields['horas_dedicadas'].initial = self.datosHistoria['horas_dedicadas']


    ESTADOS_CHOICES = [
        ('FINALIZADO', 'Finalizado'),
        ('PENDIENTE', 'Pendiente'),
        ('EN_CURSO', 'En Curso'),
        ('QUALITY_ASSURANCE', 'Quality Assurance'),
    ]

    PRIORIDAD_CHOICES = [
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
    ]

    id_historia=forms.IntegerField(disabled=True,label="ID de Historia")
    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea)
    prioridad = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=PRIORIDAD_CHOICES)
    fecha_creacion = forms.DateField(initial=datetime.date.today, disabled=True, label="Fecha de Creacion")
    horasEstimadas = forms.IntegerField(initial=0)
    estados = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=ESTADOS_CHOICES)
    horas_dedicadas = forms.IntegerField(initial=0)




class crearHistoriaForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la creacion de una Historia de usuario
    """
    # overwrite __init__
    # def __init__(self, *args, **kwargs):
    # self.request = kwargs.pop("request")  # store value of request
    ##super(crearproyectoForm,self).__init__(*args, **kwargs)
    # self.fields['creador'].initial=self.request.user.username

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
    fecha_creacion = forms.DateField(initial=datetime.date.today, disabled=True, label="Fecha de Creacion")
    horasEstimadas = forms.IntegerField(initial=0)
    estados = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=ESTADOS_CHOICES)
    horas_dedicadas = forms.IntegerField(initial=0)



