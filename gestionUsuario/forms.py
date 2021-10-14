from django import forms

class crearRolForm(forms.Form):
    """
    Formulario de creacion de roles con las opciones de 'agregar', 'borrar','modificar' y 'ver'
    """
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
