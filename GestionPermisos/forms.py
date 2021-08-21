from django import forms

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
    ##Aca debe hacerse una cosulta para filtrar a los usuarios del proyecto,
    ##estos usuarios se cargaran en un choice diccionary para poder ser usado en el campo usuario

    OPCIONES = [
        (1 , "Luis" ),
        (2 , "Leo"  ),
        (3 , "Edher")
        ]

    Roles=[
        (1,"Product Owner"),
        (2,"Scrum Master"),
        (3,"Developer")
    ]

    Usuario = forms.TypedChoiceField(label="Selecciona un usuario",choices=OPCIONES,coerce=int,widget=forms.Select)
    roles = forms.TypedChoiceField(label="Selecciona un rol",choices=Roles,coerce=int,widget=forms.RadioSelect)
