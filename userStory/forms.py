from django import forms
from django.contrib.auth.models import Group
from gestionUsuario.models import User
import datetime

from userStory.models import Historia



class crearHistoriaForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la creacion de un proyecto
    """
    # overwrite __init__
    def __init__(self, *args, **kwargs):
        self.proyecto = kwargs.pop('proyecto')  # store value of request
        super(crearHistoriaForm, self).__init__(*args, **kwargs)
        self.fields['proyecto'].initial=self.proyecto

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
    #id_historia = forms.IntegerField(disabled=True, label="ID de Historia")
    nombre = forms.CharField(max_length=150, help_text='150 characters max.')
    descripcion = forms.CharField(widget=forms.Textarea)
    prioridad = forms.ChoiceField(widget=forms.RadioSelect, choices=PRIORIDAD_CHOICES)
    fecha_creacion = forms.DateField(initial=datetime.date.today, disabled=True, label="Fecha de Creacion")
    #horasEstimadas = forms.IntegerField(initial=0, label="Horas Estimadas")
    #horas_dedicadas = forms.IntegerField(initial=0)
    proyecto=forms.IntegerField(disabled=True, label="Proyecto Propietario")

class cargarHorasHistoriaForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud para cargar las horas trabajadas en el User Story
    """
    horas = forms.IntegerField(initial=0, widget=forms.NumberInput(attrs={'type': 'number', 'id':'register-form-horas', 'name':'register-form-horas', 'value':'0', 'class':'form-control'}))
    comentario = forms.CharField(initial='', widget=forms.TextInput(attrs={'type': 'text', 'id':'register-form-comentario', 'name':'register-form-comentario', 'value':'', 'class':'form-control'}),required=False)

class seleccionarHistoriaForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud para la seleccion de la historia que se desea modificar
    """
    def __init__(self, *args, **kwargs):
        self.proyecto = kwargs.pop('proyecto')  # store value of request
        super(seleccionarHistoriaForm, self).__init__(*args, **kwargs)
        self.fields['Historia'].queryset=Historia.objects.filter(proyecto_id=self.proyecto)

    Historia = forms.ModelChoiceField(queryset=Historia.objects.all(),initial=0,label="Selecciona la historia")

class asignarEncargadoForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud para asignar una historia a un usuario
    """
    Usuario = forms.ModelChoiceField(queryset=User.objects.all().exclude(username="admin" and "Admin"), initial=0,label="Seleccione un usuario", required=True)
    Historia = forms.ModelMultipleChoiceField(queryset=Historia.objects.all(),initial=0,label="Selecciona la historia", required=True)


class modificarHistoriaForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la modificacion de un proyecto
    """
    def __init__(self, *args, **kwargs):
        self.datosHistoria = kwargs.pop("datosdelaHistoria")  # store value of request
        super(modificarHistoriaForm, self).__init__(*args, **kwargs)
        #self.fields['id_historia'].initial=self.datosHistoria['id_historia']
        self.fields['nombre'].initial = self.datosHistoria['nombre']
        self.fields['descripcion'].initial = self.datosHistoria['descripcion']
        self.fields['prioridad'].initial = self.datosHistoria['prioridad']
        #self.fields['fecha_creacion'].initial=self.datosHistoria['fecha_creacion']#este crea problema
        #self.fields['horasEstimadas'].initial = self.datosHistoria['horasEstimadas']

        #self.fields['horas_dedicadas'].initial = self.datosHistoria['horas_dedicadas']
        #self.fields['proyecto'].initial = self.datosHistoria['proyecto']


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

    #id_historia=forms.IntegerField(disabled=True,label="ID de Historia")
    #proyecto = forms.IntegerField(disabled=True, label="Proyecto Propietario")
    nombre = forms.CharField(max_length=20, help_text='20 characters max.')
    descripcion = forms.CharField(widget=forms.Textarea)
    prioridad = forms.ChoiceField(widget=forms.RadioSelect, choices=PRIORIDAD_CHOICES)
    #fecha_creacion = forms.DateField(initial=datetime.date.today, disabled=True, label="Fecha de Creacion")
    #horasEstimadas = forms.IntegerField(initial=0)

   # horas_dedicadas = forms.IntegerField(initial=0)


class eliminarHistoriaForm(forms.Form):
    """
    Implementa la clase para eliminar historia de usuario
    """
    Historia = forms.ModelChoiceField(queryset=Historia.objects.all(), initial=0,label="Seleccione Una Historia")


class asignarDesarrolladorForm(forms.Form):
    """
    Formulario de asignacion de roles a usuarios del sistema con consulta a un filtro de usuario previo
    """
    def __init__(self, *args, **kwargs):
        self.datos = kwargs.pop("developers")  # store value of request
        super(asignarDesarrolladorForm, self).__init__(*args, **kwargs)
        self.fields['encargado'].choices = self.datos['developers']

    encargado = forms.ChoiceField(required=False)



class asignaryestimarHistoria(forms.Form):
    """
    Formulario de asignacion de roles a usuarios del sistema con consulta a un filtro de usuario previo
    """
    def __init__(self, *args, **kwargs):
        self.datos = kwargs.pop("developers")  # store value of request
        super(asignaryestimarHistoria, self).__init__(*args, **kwargs)
        self.fields['encargado'].choices = self.datos['developers']

    encargado = forms.ChoiceField(required=False, widget=forms.Select( attrs={'type': 'select', 'id':'encargado','name':'encargado', 'class':'form-control'}))
    estimado = forms.IntegerField(initial=0, widget=forms.NumberInput(
        attrs={'type': 'number', 'id': 'estimado', 'name': 'estimado', 'value': '0',
               'class': 'form-control'}))




