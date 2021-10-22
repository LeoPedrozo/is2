from Sprints.models import Sprint
from gestionUsuario.models import User
from userStory.models import Historia
import django_filters


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]

class HistoriaFilter(django_filters.FilterSet):
    class Meta:
        model = Historia
        fields = ['prioridad','estados','encargado', ]

class SprintFilter(django_filters.FilterSet):
    class Meta:
        model = Sprint
        fields = ['estados']
