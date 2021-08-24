from django import forms

from django.contrib.auth.models import Group
from gestionUsuario.models import User

class crearRolForm(forms.Form):
    Rol = forms.CharField()
    OPTIONS = (
        ("add", "Agregar"),
        ("delete", "Borrar"),
        ("change","Modificar"),
        ("view","Ver"),
    )
    Historia = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=OPTIONS)
    Proyecto = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=OPTIONS)
    Sprint = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=OPTIONS)


class asignarRolForm(forms.Form):
    ##Aca debe hacerse una cosulta para filtrar a los usuarios
    ##estos usuarios se cargaran en un choice diccionary para poder ser usado en el campo usuario
    Usuario = forms.ModelChoiceField(queryset=User.objects.all().exclude(username="admin"), initial=0)
    Roles = forms.ModelChoiceField(queryset=Group.objects.all(),initial=0)
