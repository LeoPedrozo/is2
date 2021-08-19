from django.contrib import admin

# Register your models here.
from .models import Proyecto, Sprint

admin.site.register(Proyecto)
admin.site.register(Sprint)

