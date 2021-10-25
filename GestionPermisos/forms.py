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
    # overwrite __init__
    def __init__(self, *args, **kwargs):
        self.datos = kwargs.pop("proyecto")  # store value of request
        super(asignarRolForm, self).__init__(*args, **kwargs)
        #self.fields['Usuario'].queryset = User.objects.filter(proyecto_id=self.datos['id_proyecto']).exclude(username="admin")
        self.fields['Usuario'].choices = self.datos['usuario_names']
        self.fields['Roles'].choices = self.datos['roles_name']

    #Usuario = forms.ModelChoiceField(queryset=User.objects.all().exclude(username="admin"))
    Usuario = forms.ChoiceField()
    Roles = forms.ChoiceField()


#class seleccionarRolForm(forms.Form):
#    Rol = forms.ModelChoiceField(queryset=Group.objects.all().exclude(name="registrado"), initial=0,label="Seleccione Rol")

class seleccionarRolForm(forms.Form):
    """
    Formulario de seleccion de roles del sistema
    """
    def __init__(self, *args, **kwargs):
        self.datos = kwargs.pop("proyecto")  # store value of request
        super(seleccionarRolForm, self).__init__(*args, **kwargs)
        self.fields['Rol'].choices = self.datos['roles_name']
    Rol = forms.ChoiceField()




class modificarRolForm(forms.Form):
    """
    Formulario de modificacion de roles con las opciones de 'agregar', 'borrar','modificar' y 'ver'
    """
    # overwrite __init__
    def __init__(self, *args, **kwargs):
        self.datos = kwargs.pop("datosdelRol")  # store value of request

        super(modificarRolForm, self).__init__(*args, **kwargs)
        self.fields['RolName'].initial = self.datos['nombreRol']
        self.fields['Proyecto'].initial=self.datos['Proyecto']
        self.fields['Historia'].initial = self.datos['Historia']
        self.fields['Sprint'].initial = self.datos['Sprint']



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
    """
    Formulario para habilitar o restringir acceso al sistema
    """
    estados=(
        (True,"Habilitar acceso al sistema"),
        (False,"Restringir acceso al sistema"),
    )
    Usuario = forms.ModelChoiceField(queryset=User.objects.all().exclude(username="admin" and "Admin"), initial=0,label="Seleccione un usuario")
    Habilitado = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=estados,label="Usted desea?")




