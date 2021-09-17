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
        #self.fields['creador'].initial=self.request.user.username
        sprintNumber = forms.IntegerField(label="Numero de Sprint")
        fecha_inicio =forms.DateField(initial=datetime.date.today, disabled=True, label="Fecha de Inicio")
        fecha_fin = forms.DateField(initial=datetime.date.today, label="Fecha fin")
        historias =forms.ModelMultipleChoiceField(queryset=Historia.objects.all(),label="Selecciona historia",blank=True,initial=None)
