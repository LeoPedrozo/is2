from django import forms
from django.contrib.auth.models import Group
from gestionUsuario.models import User
from proyectos.models import Proyecto
import datetime



class crearproyectoForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la creacion de un proyecto
    """
    # overwrite __init__
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  # store value of request
        super(crearproyectoForm,self).__init__(*args, **kwargs)
        self.fields['creador'].initial=self.request.user.username

    estados = (
        ('PENDIENTE', 'Pendiente'),
        ('INICIADO', 'Iniciado'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    )

    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea)
    creador = forms.CharField(disabled=True)
    estado = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=estados)

    fecha = forms.DateField(initial=datetime.date.today,disabled=True,label="Fecha de Creacion")
    fecha_entrega = forms.DateField(initial=datetime.date.today,label="Fecha de Entrega")
    miembros = forms.ModelMultipleChoiceField(queryset=User.objects.all().exclude(username=["admin","Admin"]), initial=0)


# crear formualrios de  modificar y eliminar proyecto.
# el campo de miembros pierde el estado original, se solucionaria si el modelo de proyecto si tenga un campo de miembros

class modificarproyectoForm(forms.Form):
    """
      Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la modificacion de un proyecto
      """

    # overwrite __init__
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  # store value of request

        super(modificarproyectoForm, self).__init__(*args, **kwargs)
        self.fields['creador'].initial = self.request.user.username
        self.fields['nombre'].initial=self.request.user.proyecto.nombre
        self.fields['descripcion'].initial=self.request.user.proyecto.descripcion
        self.fields['estado'].initial=self.request.user.proyecto.estado
        self.fields['fecha'].initial=self.request.user.proyecto.fecha
        self.fields['fecha_entrega'].initial=self.request.user.proyecto.fecha_entrega
        self.fields['id'].initial=self.request.user.proyecto_id
        self.fields['miembros'].queryset=User.objects.filter(proyecto_id=self.request.user.proyecto_id).exclude(username='admin')

    estados = (
        ('PENDIENTE', 'Pendiente'),
        ('INICIADO', 'Iniciado'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    )


    id=forms.IntegerField(disabled=True,label="ID del proyecto")
    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea)
    creador = forms.CharField(disabled=True)
    estado = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=estados)

    fecha = forms.DateField(initial=datetime.date.today, disabled=True, label="Fecha de Creacion")
    fecha_entrega = forms.DateField(initial=datetime.date.today, label="Fecha de Entrega")
    miembros = forms.ModelMultipleChoiceField(required=False,queryset=User.objects.filter().exclude(username="admin"), label="Eliminar miembros [Los usuarios seleccionados seran eliminados]",label_suffix="Miembros del proyecto")
    usuarios= forms.ModelMultipleChoiceField(required=False,queryset=User.objects.filter(proyecto_id__isnull=True).exclude(username='admin'),label="Agregar Nuevos usuarios",label_suffix="lista de usuarios disponibles")


class eliminarProyectoForm(forms.Form):
    Proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all(), initial=0,label="Seleccione algun proyecto")


