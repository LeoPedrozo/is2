from time import strptime
from datetime import datetime

from django import forms
import datetime
from userStory.models import Historia


class crearSprintForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la creacion de un sprint con los
    campos de 'numero sprint', 'fecha de inicio', 'fecha fin' e 'historias'
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  # store value of request
        super(crearSprintForm, self).__init__(*args, **kwargs)
        self.fields['idproyecto'].initial = self.request['proyecto']
        self.fields['historias'].queryset = Historia.objects.filter(proyecto=self.request['proyecto'],estados="PENDIENTE")

    idproyecto = forms.IntegerField(label="Proyecyo Propietario",disabled=True)
    sprintNumber = forms.IntegerField(label="Numero de Sprint")
    fecha_inicio =forms.DateField(initial=datetime.date.today, disabled=True, label="Fecha de Inicio")
    fecha_fin = forms.DateField(initial=datetime.date.today, label="Fecha fin")
    historias =forms.ModelMultipleChoiceField(queryset=Historia.objects.all(),label="Selecciona historia",blank=True,initial=None)

class modificarSprintForm(forms.Form):
        """
        Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la creacion de un sprint con los
        campos de 'numero sprint', 'fecha de inicio', 'fecha fin' e 'historias'
        """
        def __init__(self, *args, **kwargs):
                self.request = kwargs.pop("request")  # store value of request
                super(modificarSprintForm, self).__init__(*args, **kwargs)
       # self.fields['creador'].initial=self.request.user.username
                self.fields['id'].initial=self.request['id']
                self.fields['proyecto'].initial=self.request['proyecto']
                self.fields['sprintNumber'].initial=self.request['sprintNumber']
                self.fields['historias'].queryset=Historia.objects.filter(pk__in=self.request['historias'])
                self.fields['fecha_inicio'].initial = datetime.datetime.strptime(self.request['fecha_inicio'],"%Y/%m/%d")
                self.fields['fecha_fin'].initial = datetime.datetime.strptime(self.request['fecha_fin'],"%Y/%m/%d")

        id=forms.IntegerField(label="ID de sprint",disabled=True)
        proyecto = forms.IntegerField(label="Proyecto Propietario", disabled=True)
        sprintNumber = forms.IntegerField(label="Numero de Sprint",disabled=True)
        #autovalor
        fecha_inicio =forms.DateField(disabled=True, label="Fecha de Inicio")
        #dato modificable
        fecha_fin = forms.DateField(label="Fecha fin")
        #Las historias seleccioandas se ignorara durante el sprint
        historias =forms.ModelMultipleChoiceField(queryset=Historia.objects.all(),label="Selecciona historia",blank=True,initial=None,required=False)


class visualizarSprintForm(forms.Form):
    """
    Implementa la clase para ejecutar un formulario de solicitud de datos necesarios para la visualizacion de un sprint con los
    campos de 'numero sprint', 'fecha de inicio', 'fecha fin' e 'historias'
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
    fecha_fin = forms.DateField(initial=datetime.date.today, label="Fecha fin", disabled=True)

    # Las historias seleccioandas se ignorara durante el sprint
    historias = forms.ModelChoiceField(empty_label= "Despliegue las historias", queryset=Historia.objects.all(), label="Historias",
                                               blank=True, initial=None)
