from django import forms

from django.contrib.auth.models import Group
from gestionUsuario.models import User

class crearRolForm(forms.Form):
    """
    Formulario de creacion de roles con las opciones de 'agregar', 'borrar','modificar' y 'ver'
    """


    OPTIONS = (
        ("add", "Agregar"),
        ("delete", "Borrar"),
        ("change","Modificar"),
        ("view","Ver"),
    )
    RolName = forms.CharField(required=True,label="Nombre del Rol")
    Historia = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=OPTIONS)
    Proyecto = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=OPTIONS)
    Sprint = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=OPTIONS)


class asignarRolForm(forms.Form):
    """
    Formulario de asignacion de roles a usuarios del sistema con consulta a un filtro de usuario previo
    """
    ##Aca debe hacerse una cosulta para filtrar a los usuarios
    ##estos usuarios se cargaran en un choice diccionary para poder ser usado en el campo usuario
    Usuario = forms.ModelChoiceField(queryset=User.objects.all().exclude(username="admin"), initial=0)
    Roles = forms.ModelChoiceField(queryset=Group.objects.all(),initial=0)



class seleccionarRolForm(forms.Form):
    Rol = forms.ModelChoiceField(queryset=Group.objects.all(), initial=0,label="Seleccione Rol")





class modificarRolForm(forms.Form):
    """
    Formulario de creacion de roles con las opciones de 'agregar', 'borrar','modificar' y 'ver'
    """
    # overwrite __init__
    def __init__(self, *args, **kwargs):
        self.datos = kwargs.pop("datosdelRol")  # store value of request

        super(modificarRolForm, self).__init__(*args, **kwargs)
        self.fields['RolName'].initial = self.datos



    OPTIONS = (
        ("add", "Agregar"),
        ("delete", "Borrar"),
        ("change","Modificar"),
        ("view","Ver"),
    )
    RolName = forms.CharField(required=True,label="Nombre del Rol")
    Historia = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=OPTIONS)
    Proyecto = forms.MultipleChoiceField(required=False,widget=forms.CheckboxSelectMultiple, choices=OPTIONS)
    Sprint = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=OPTIONS)








class crearUsuarioForm(forms.Form):
    """
    Formulario de creacion de usuarios del sistema, solicitando el nombre y correo
    """
    Nombre= forms.CharField()
    correo= forms.CharField()


class registroDeUsuariosForm(forms.Form):
    """Formulario para habilitacion de usuarios dentro del sistema

    """
    estados=(
        (True,"Habilitar acceso al sistema"),
        (False,"Restringir acceso al sistema"),
    )
    Usuario = forms.ModelChoiceField(queryset=User.objects.all().exclude(username="admin" and "Admin"), initial=0,label="Seleccione un usuario")
    Habilitado = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=estados,label="Usted desea?")




