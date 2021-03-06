from django import forms
from django.contrib.auth.models import Group
from gestionUsuario.models import User
from proyectos.models import Proyecto
import datetime
from functools import partial
from django.forms import fields
DateInput = partial(forms.DateInput, {'class': 'datepicker'})



class crearproyectoForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario donde se solicitan los datos necesarios para la creacion de un proyecto
    """

    # overwrite __init__
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  # store value of request
        super(crearproyectoForm,self).__init__(*args, **kwargs)
        self.fields['miembros'].choices=self.request['miembros']

    estados = (
        ('PENDIENTE', 'Pendiente'),
        ('INICIADO', 'Iniciado'),
        #('FINALIZADO', 'Finalizado'),
        #('CANCELADO', 'Cancelado'),
    )

    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea)
    estado = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=estados)

    fecha = forms.DateField(widget=DateInput(),input_formats=['%Y/%m/%d'],initial=datetime.date.today,label="Fecha inicio Estimado")
    fecha_entrega = forms.DateField(widget=DateInput(),input_formats=['%Y/%m/%d'],initial=datetime.date.today,label="Fecha de Finalizacion Estimada")
    #miembros = forms.ModelMultipleChoiceField(queryset=User.objects.all().exclude(username=["admin","Admin"]),initial=0)
    #miembros = UserModelMultipleChoiceField(queryset=User.objects.all().exclude(username=["admin", "Admin"]),
    #                                          initial=0)
    miembros = forms.MultipleChoiceField(label="Lista de usuarios disponibles")
# crear formualrios de  modificar y eliminar proyecto.
# el campo de miembros pierde el estado original, se solucionaria si el modelo de proyecto si tenga un campo de miembros

class modificarproyectoForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario donde se solicitan los datos necesarios para modificar un proyecto
    """

    # overwrite __init__
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  # store value of request
        super(modificarproyectoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].initial = self.request['Proyecto']
        self.fields['descripcion'].initial = self.request['Descripcion']
        self.fields['estado'].initial = self.request['estado']
        self.fields['fecha'].initial = datetime.datetime.strptime(self.request['fecha'], "%Y/%m/%d")
        self.fields['fecha_entrega'].initial = datetime.datetime.strptime(self.request['fecha_entrega'], "%Y/%m/%d")
        self.fields['id'].initial = self.request['Proyecto_id']
        #Esto debe cambiar
        self.fields['miembros'].choices = self.request['miembros']
        #self.fields['usuarios'].queryset = User.objects.all().exclude(username='admin',proyectos_asociados__proyectos__proyecto_id=self.request['Proyecto_id'])
        self.fields['usuarios'].choices = self.request['usuarios']

    estados = (
        ('PENDIENTE', 'Pendiente'),
        ('INICIADO', 'Iniciado'),
       # ('FINALIZADO', 'Finalizado'),
       # ('CANCELADO', 'Cancelado'),
    )


    id=forms.IntegerField(disabled=True,label="ID del proyecto")
    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea)
    estado = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=estados)

    fecha = forms.DateField(initial=datetime.date.today, disabled=True, label="Fecha de Inicio")
    fecha_entrega = forms.DateField(widget=DateInput(),input_formats=['%Y/%m/%d'],initial=datetime.date.today, label="Fecha de Finalizacion")
    miembros = forms.MultipleChoiceField(required=False, label="Eliminar miembros [Los usuarios seleccionados seran eliminados]",label_suffix="Miembros del proyecto")
    #usuarios= forms.ModelMultipleChoiceField(required=False,queryset= User.objects.all(),label="Agregar Nuevos usuarios",label_suffix="lista de usuarios disponibles")
    usuarios= forms.MultipleChoiceField(required=False, label="Agregar Nuevos usuarios",label_suffix="lista de usuarios disponibles")

class seleccionarProyectoForm(forms.Form):
    """
    Implementa un formulario que posibilita seleccionar un proyecto de varios disponibles
    """

    Proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all(), initial=0,label="Seleccione algun proyecto")



class importarRolForm(forms.Form):
    """
    Implementa un formulario que permite importar roles definidos de un proyecto a otro
    """

    ProyectoA = forms.ModelChoiceField(queryset=Proyecto.objects.all(), initial=0, label="Importar Roles del proyecto")
    ProyectoB = forms.ModelChoiceField(queryset=Proyecto.objects.all(), initial=0, label="al proyecto")