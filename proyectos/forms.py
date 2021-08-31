from django import forms
from django.contrib.auth.models import Group
from gestionUsuario.models import User


class step1_crearproyectoForm(forms.Form):
    estados = (
        ("iniciar","Iniciar al finalizar la configuracion"),
        ("esperar","Iniciar cuando se indique en la configuracion del proyecto"),
        ("finalizar","Finalizado"),
        ("qualityc","Quality check"),
    )

    nombre = forms.CharField()
    descripcion = forms.Textarea()
    creador = forms.CharField()
    estado = forms.MultipleChoiceField(required=False, widget=forms.RadioSelect, choices=estados)
    fecha_creado = forms.DateField()
    miembros = forms.ModelMultipleChoiceField(queryset=User.objects.all().exclude(username="admin"), initial=0)



#class step3_asignarrolesForm(forms.Form):
 #   Miembro = forms.ModelChoiceField(queryset=User.objects.all().exclude(username="admin"), initial=0)
  #  Roles = forms.ModelChoiceField(queryset=Group.objects.all(), initial=0)

