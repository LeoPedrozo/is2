from django import forms
import datetime
from userStory.models import Historia
class crearSprintForm(forms.Form):

        #self.fields['creador'].initial=self.request.user.username
        sprintNumber = forms.IntegerField(label="Numero de Sprint")
        fecha_inicio =forms.DateField(initial=datetime.date.today, disabled=True, label="Fecha de Inicio")
        fecha_fin = forms.DateField(initial=datetime.date.today, label="Fecha fin")
        historias =forms.ModelMultipleChoiceField(queryset=Historia.objects.all(),initial=0)
