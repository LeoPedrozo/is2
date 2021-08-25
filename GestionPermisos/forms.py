from django import forms

from django.contrib.auth.models import Group
from gestionUsuario.models import User

class crearRolForm(forms.Form):
    """Formulario de creacion de roles con las opciones de 'agregar', 'borrar','modificar' y 'ver'"""

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
    """Formulario de asignacion de roles a usuarios del sistema con consulta a un filtro de usuario previo"""

    ##Aca debe hacerse una cosulta para filtrar a los usuarios
    ##estos usuarios se cargaran en un choice diccionary para poder ser usado en el campo usuario
    Usuario = forms.ModelChoiceField(queryset=User.objects.all().exclude(username="admin"), initial=0)
    Roles = forms.ModelChoiceField(queryset=Group.objects.all(), initial=0)
