from Sprints.models import Sprint
from gestionUsuario.models import User
from userStory.models import Historia
from proyectos.models import Proyecto
import django_filters


class UserFilter(django_filters.FilterSet):
    """
    Clase que implementa la busqueda de un usuario con las opciones de filtrado: 'username', 'first_name' y 'last_name'
    """

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]


class HistoriaFilter(django_filters.FilterSet):
    """
    Clase que implementa la busqueda de un user story con las opciones de filtrado: 'prioridad', 'estados' y 'encargado'
    """

    class Meta:
        model = Historia
        fields = ['prioridad','estados','encargado', ]


class SprintFilter(django_filters.FilterSet):
    """
    Clase que implementa la busqueda de un sprint con la opcion de filtrar por: 'estados'
    """

    class Meta:
        model = Sprint
        fields = ['estados']

class ProyectoFilter(django_filters.FilterSet):
    class  Meta:
        model=Proyecto
        fields= ['estado']
