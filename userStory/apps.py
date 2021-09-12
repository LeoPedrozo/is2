from django.apps import AppConfig


class UserstoryConfig(AppConfig):
    """Clase para configurar algunos de los atributos de la aplicación.
        En esta:
         - El tipo predeterminado de clave primaria: Un entero de 64 bits
         - El nombre de la aplicacion: userStory"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userStory'
