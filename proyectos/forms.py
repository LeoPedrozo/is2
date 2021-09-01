from django import forms
from django.contrib.auth.models import Group
from gestionUsuario.models import User
import datetime




class crearproyectoForm(forms.Form):
    # overwrite __init__
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  # store value of request
        super(crearproyectoForm,self).__init__(*args, **kwargs)
        self.fields['creador'].initial=self.request.user.username

    estados = (
        ("iniciar","Iniciar al finalizar la configuracion"),
        ("esperar","Iniciar cuando se indique en la configuracion del proyecto"),
        ("finalizar","Finalizado"),
        ("qualityc","Quality check"),
    )

    nombre = forms.CharField()
    descripcion = forms.CharField(widget=forms.Textarea)
    creador = forms.CharField(disabled=True)
    estado = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=estados)

    fecha = forms.DateField(initial=datetime.date.today,disabled=True,label="Fecha de Creacion")
    fecha_entrega = forms.DateField(initial=datetime.date.today,label="Fecha de Entrega")
    miembros = forms.ModelMultipleChoiceField(queryset=User.objects.all().exclude(username="admin"), initial=0)



#class step3_asignarrolesForm(forms.Form):
 #   Miembro = forms.ModelChoiceField(queryset=User.objects.all().exclude(username="admin"), initial=0)
  #  Roles = forms.ModelChoiceField(queryset=Group.objects.all(), initial=0)

