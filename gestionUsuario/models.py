from django.db import models
import datetime

# Create your models here.




""" Registra los datos del usuario logeado en el sistema """
class UsuarioLogeo(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    correo = models.EmailField()
    fecha = models.DateTimeField()

    def __str__(self):
        return f"El usuario {self.nombre} {self.apellido} ha loggeado con el correo {self.correo} fecha:{self.fecha.day}/{self.fecha.month}/{self.fecha.year}-{self.fecha.hour}:{self.fecha.minute}:{self.fecha.second}"