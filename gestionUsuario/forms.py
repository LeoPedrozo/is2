from django import forms

class asignarcapacidadForm(forms.Form):
    """
    Clase que implementa un formulario para la asignacion de capacidad, requisito necesario para el sprint planning
    """

    capacidad = forms.IntegerField(initial=0, widget=forms.NumberInput(
        attrs={'type': 'number', 'id': 'register-form-horas', 'name': 'register-form-horas', 'value': '0',
               'class': 'form-control'}))