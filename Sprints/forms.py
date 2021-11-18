from time import strptime
from datetime import datetime

from django import forms
import datetime
from userStory.models import Historia
from functools import partial
from bootstrap_daterangepicker import widgets, fields


DateInput = partial(forms.DateInput, {'class': 'datepicker'})




class crearSprintForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud de datos que son necesarios para la creacion de un sprint, el
    formulario solicita los campos: 'numero sprint', 'fecha de inicio', 'fecha fin'
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  # store value of request
        super(crearSprintForm, self).__init__(*args, **kwargs)
        self.fields['idproyecto'].initial = self.request['proyecto']
        self.fields['rango'].initial = self.request['rango']
        # self.fields['historias'].queryset = Historia.objects.filter(proyecto=self.request['proyecto'],estados="")

    idproyecto = forms.IntegerField(label="Proyecto Propietario", disabled=True)
    sprintNumber = forms.IntegerField(label="Numero de Sprint", required=True)

    rango=forms.CharField(disabled=True,label="Rango de Fecha Valida")
    fecha_inicio = forms.DateField(widget=DateInput(), input_formats=['%Y/%m/%d'],initial=datetime.date.today, label="Fecha de Inicio")
    fecha_fin = forms.DateField(widget=DateInput(), input_formats=['%Y/%m/%d'], initial=datetime.date.today,
                                label="Fecha de Finalizacion")

    # historias =forms.ModelMultipleChoiceField(queryset=Historia.objects.all(),label="Selecciona historia",blank=True,initial=None,required=False)



class modificarSprintForm(forms.Form):
    """
        Implementa la clase para ejecutar un formulario de solicitud de datos que son necesarios para la creacion de un sprint, el
        formulario permite modificar los campos: 'numero sprint', 'fecha de inicio', 'fecha fin'
        """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  # store value of request
        super(modificarSprintForm, self).__init__(*args, **kwargs)
        self.fields['id'].initial = self.request['id']
        self.fields['proyecto'].initial = self.request['proyecto']
        self.fields['sprintNumber'].initial = self.request['sprintNumber']
        # self.fields['historias'].queryset=Historia.objects.filter(pk__in=self.request['historias'])
        self.fields['fecha_inicio'].initial = datetime.datetime.strptime(self.request['fecha_inicio'], "%Y/%m/%d")
        self.fields['fecha_fin'].initial = datetime.datetime.strptime(self.request['fecha_fin'], "%Y/%m/%d")
        self.fields['rango'].initial=self.request['rango']

    id = forms.IntegerField(label="ID de sprint", disabled=True)
    proyecto = forms.IntegerField(label="Proyecto Propietario", disabled=True)
    sprintNumber = forms.IntegerField(label="Numero de Sprint", disabled=True)
    # autovalor
    rango=forms.CharField(disabled=True,  label="Rango Permitido")
    fecha_inicio = forms.DateField(widget=DateInput(),input_formats=['%Y/%m/%d'],label="Fecha de Inicio")
    # dato modificable
    fecha_fin = forms.DateField(widget=DateInput(), input_formats=['%Y/%m/%d'], label="Fecha fin")
    # Las historias seleccioandas se ignorara durante el sprint


class visualizarSprintForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la visualizacion de un sprint con los
    campos de 'numero sprint', 'fecha de inicio', 'fecha fin'
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  # store value of request
        super(visualizarSprintForm, self).__init__(*args, **kwargs)
        # self.fields['creador'].initial=self.request.user.username
        self.fields['id'].initial = self.request['id']
        self.fields['proyecto'].initial = self.request['proyecto']
        self.fields['sprintNumber'].initial = self.request['sprintNumber']
        self.fields['historias'].queryset = Historia.objects.filter(pk__in=self.request['historias'])

    id = forms.IntegerField(label="ID de sprint", disabled=True)
    proyecto = forms.IntegerField(label="Proyecto Propietario", disabled=True)
    sprintNumber = forms.IntegerField(label="Numero de Sprint", disabled=True)
    # autovalor
    fecha_inicio = forms.DateField(initial=datetime.date.today, disabled=True, label="Fecha de Inicio")
    # dato modificable
    fecha_fin = forms.DateField(label="Fecha fin", disabled=True)

    # Las historias seleccioandas se ignorara durante el sprint
    historias = forms.ModelChoiceField(empty_label="Despliegue las historias", queryset=Historia.objects.all(),
                                       label="Historias",
                                       blank=True, initial=None)


class seleccionarSprintForm(forms.Form):
    """
    Implementa un formulario que permite seleccionar un sprint de una lista de sprints del proyecto
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("listaSprint")  # store value of request
        super(seleccionarSprintForm, self).__init__(*args, **kwargs)
        self.fields['sprint'].choices = self.request

    sprint = forms.ChoiceField(label="Seleccione el Sprint")


#class extenderSprintForm(forms.Form):

#    """
#    Implementa la clase para ejecutar un formulario que permite la entrada de una nueva fecha de finalizacion estimada
#    """

#    def __init__(self, *args, **kwargs):
#        self.dato = kwargs.pop("dato")  # store value of request
#        super(extenderSprintForm, self).__init__(*args, **kwargs)
#        self.fields['fecha_fin'].initial = datetime.datetime.strptime(self.dato['fecha_fin'], "%Y/%m/%d")#
#
#    fecha_fin = forms.DateField(widget=DateInput(), input_formats=['%Y/%m/%d'], label="Fecha fin")

class extenderSprintForm(forms.Form):
   """
   Implementa la clase para ejecutar un formulario que permite la entrada de una nueva fecha de finalizacion estimada
   """

   def __init__(self, *args, **kwargs):
       self.dato = kwargs.pop("dato")  # store value of request
       super(extenderSprintForm, self).__init__(*args, **kwargs)
       self.fields['fecha_fin'].initial = datetime.datetime.strptime(self.dato['fecha_fin'], "%Y/%m/%d")
   #fecha_fin = forms.DateField(widget=DateInput(), input_formats=['%Y/%m/%d'], label="Fecha fin")
   fecha_fin = fields.DateField(
        input_formats=['%Y/%m/%d'],
        widget=widgets.DatePickerWidget(
            format='%Y/%m/%d'
        ),label="Fecha fin")


class intercambiardeveloperForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario que permite intercambiar desarrolladores de un sprint con otros
    pertenecientes al mismo proyecto
    """
    def __init__(self, *args, **kwargs):
        self.dato = kwargs.pop("dato")  # store value of request
        super(intercambiardeveloperForm, self).__init__(*args, **kwargs)
        self.fields['miembroA'].choices = self.dato['equipo']
        self.fields['miembroB'].choices = self.dato['disponibles']

    miembroA = forms.ChoiceField(label="Miembros de este sprint")
    miembroB = forms.ChoiceField(label="Miembros de este proyecto")
